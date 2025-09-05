from temperature_loader import get_combined_data
import pandas as pd

# Load the temperature data using the temperature loader
combined_df = get_combined_data("temperatures")
print(f"Loaded data shape: {combined_df.shape}")
print("Sample data:")
print(combined_df.head())

# Calculate standard deviation for each station to measure temperature stability
station_stability = combined_df.groupby('STATION_NAME')['Temperature'].std()
print("Standard deviation calculated for each station")
print(f"Number of stations analyzed: {len(station_stability)}")

# Check some sample results to verify the calculation worked
print("\nSample standard deviations:")
print(station_stability.head())

# Find the most stable station (lowest standard deviation)
min_std = station_stability.min()
most_stable_stations = station_stability[station_stability == min_std]

# Find the most variable station (highest standard deviation)  
max_std = station_stability.max()
most_variable_stations = station_stability[station_stability == max_std]

print(f"Most stable temperature (lowest std dev): {min_std:.2f}°C")
print(f"Most variable temperature (highest std dev): {max_std:.2f}°C")
print(f"\nNumber of most stable stations: {len(most_stable_stations)}")
print(f"Number of most variable stations: {len(most_variable_stations)}")

# Show which specific stations are the most stable and most variable
print("Most stable station:")
for station_name, std_dev in most_stable_stations.items():
    print(f"{station_name}: {std_dev:.2f}°C standard deviation")

print("\nMost variable station:")
for station_name, std_dev in most_variable_stations.items():
    print(f"{station_name}: {std_dev:.2f}°C standard deviation")
    
# Save results to the required output file in the specified format
with open("temperature_stability_stations.txt", "w") as f:
    # Stations with the most stable temperatures
    for station_name, std_dev in most_stable_stations.items():
        f.write(f"Most Stable: Station {station_name}: StdDev {std_dev:.1f}°C\n")
    
    # Stations with the most variable temperatures  
    for station_name, std_dev in most_variable_stations.items():
        f.write(f"Most Variable: Station {station_name}: StdDev {std_dev:.1f}°C\n")

print("Temperature stability results saved to temperature_stability_stations.txt")