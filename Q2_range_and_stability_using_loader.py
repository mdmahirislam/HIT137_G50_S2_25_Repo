# Q2_range_and_stability_using_loader.py
import statistics, math, re
from pathlib import Path

MONTHS_FULL = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]
MONTHS_ABBR = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
MONTH_KEYS   = {m.lower() for m in MONTHS_FULL + MONTHS_ABBR}

OUT_RANGE = Path("range_stations.txt")
OUT_STAB  = Path("temperature_stability_stations.txt")

def norm(s): return re.sub(r'[^a-z0-9]+', '', (s or '').strip().lower())
def to_float(x):
    try: return float(re.sub(r'[^\d\.\-\+eE]', '', str(x)))
    except: return math.nan

def normalize_from_dict(data: dict) -> dict[str, list[float]]:
    # Accept {station: [floats]} or {station: [dicts with month->value]}
    out = {}
    for s, vals in data.items():
        buf = []
        for v in vals:
            if isinstance(v,(int,float)): buf.append(float(v))
            elif isinstance(v,dict):
                for k,val in v.items():
                    if norm(k) in MONTH_KEYS:
                        f = to_float(val)
                        if not math.isnan(f): buf.append(f)
        if buf: out[s] = buf
    return out

def normalize_from_rows(rows_iter) -> dict[str, list[float]]:
    out = {}
    for row in rows_iter:
        if not isinstance(row, dict): continue
        s = row.get("STATION_NAME") or row.get("Station") or row.get("station") or row.get("station_name")
        if not s: continue
        # case A: long format with Temperature column
        tkey = None
        for k in row.keys():
            if norm(k) in ("temperature","temp"):
                tkey = k; break
        if tkey:
            f = to_float(row.get(tkey))
            if not math.isnan(f): out.setdefault(s, []).append(f)
            continue
        # case B: wide format with month columns
        for k,v in row.items():
            if norm(k) in MONTH_KEYS:
                f = to_float(v)
                if not math.isnan(f): out.setdefault(s, []).append(f)
    return out

def load_with_temperature_loader():
    import temperature_loader as TL  # your file in the repo
    # try common function names, with and without a 'temperatures' path
    for name in ("load_temperatures","load_all","load_data","load"):
        if hasattr(TL, name):
            fn = getattr(TL, name)
            for arg in ((), ("temperatures",)):
                try:
                    data = fn(*arg)
                except TypeError:
                    continue
                # normalize various shapes
                if isinstance(data, dict):
                    st = normalize_from_dict(data)
                    if st: return st
                # try iterables of dict rows
                try:
                    st = normalize_from_rows(iter(data))
                    if st: return st
                except Exception:
                    pass
    raise RuntimeError(
        "temperature_loader.py is present, but I couldn't find a usable function "
        "(looked for load_temperatures/load_all/load_data/load). "
        "Update the script with the correct function name if needed."
    )

def compute_and_write(stations: dict[str, list[float]]):
    stations = {s:v for s,v in stations.items() if v}
    ranges = {s:(max(v)-min(v)) for s,v in stations.items()}
    max_r = max(ranges.values())
    winners = [s for s,r in ranges.items() if abs(r-max_r)<1e-12]
    with OUT_RANGE.open("w", encoding="utf-8") as f:
        f.write(f"Largest temperature range: {max_r:.2f}°C\n")
        for s in winners: f.write(f"{s}\n")

    stdevs = {s: statistics.pstdev(v) for s,v in stations.items() if len(v)>=2}
    if not stdevs:
        OUT_STAB.write_text("Not enough data to compute standard deviation (need ≥2 values per station).\n", encoding="utf-8")
        return
    mn, mx = min(stdevs.values()), max(stdevs.values())
    most_stable   = [s for s,sd in stdevs.items() if abs(sd-mn)<1e-12]
    most_variable = [s for s,sd in stdevs.items() if abs(sd-mx)<1e-12]
    with OUT_STAB.open("w", encoding="utf-8") as f:
        for s in most_stable:   f.write(f"Most Stable: {s} — StdDev {mn:.2f}°C\n")
        for s in most_variable: f.write(f"Most Variable: {s} — StdDev {mx:.2f}°C\n")

if __name__ == "__main__":
    stations = None
    try:
        stations = load_with_temperature_loader()
    except Exception as e:
        print("Loader not used:", e)
        # Fallback: import the plain parser you already added
        try:
            from Q2_range_and_stability import load_station_temps
            stations = load_station_temps(Path("temperatures"))
        except Exception:
            raise SystemExit("Could not use temperature_loader and no fallback available.")
    compute_and_write(stations)
    print("Wrote range_stations.txt and temperature_stability_stations.txt")
