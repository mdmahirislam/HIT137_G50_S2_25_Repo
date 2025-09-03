from temperature_loader import get_combined_data
import pandas as pd

# Load all data
combined_df = get_combined_data("temperatures")
print("Data loaded:", combined_df.shape)
print(combined_df.head())

# Map months to seasons
def get_season_from_month(month):
    if month in (1, 2 , 12):
        return "Summer"
    if month in (3, 4, 5):
        return "Autumn"
    if month in (6, 7, 8):
        return "Winter"
    if month in (9, 10, 11):
        return "Spring"

# Apply the mapping
combined_df["Season"] = combined_df["Month_Num"].apply(get_season_from_month)

print(combined_df.head(15))  # check if Season column looks right

# Calculate average temperature for each season (across all stations and years)
seasonal_avg = combined_df.groupby("Season")["Temperature"].mean().round(2)

print("Seasonal Averages:")
print(seasonal_avg)

# Save results to a text file
with open("average_temp.txt", "w") as f:
    for season, avg in seasonal_avg.items():
        f.write(f"{season}: {avg:.1f}°C\n")

print("Seasonal averages saved to average_temp.txt")

