from temperature_loader import get_combined_data
import pandas as pd

# Load your data
combined_df = get_combined_data("temperatures")
print("Data shape:", combined_df.shape)
print("Sample data:")
print(combined_df.head())

# Group by station to analyze each one separately
station_groups = combined_df.groupby('STATION_NAME')

# Check how many stations we're working with
print("Number of unique stations:", len(station_groups))

# Test with one station to verify the logic works
sample_station = combined_df[combined_df['STATION_NAME'] == 'ADELAIDE-KENT-TOWN']
print("\nADELAIDE-KENT-TOWN temperatures:")
print("Number of temperature readings:", len(sample_station))
print("Temperature range for this station:")
print("Min:", sample_station['Temperature'].min())
print("Max:", sample_station['Temperature'].max())
print("Range:", sample_station['Temperature'].max() - sample_station['Temperature'].min())

# Calculate min, max, and range for each station across all years
station_stats = combined_df.groupby('STATION_NAME')['Temperature'].agg(['min', 'max'])
station_stats['range'] = station_stats['max'] - station_stats['min']

# Display the results sorted by range (largest first)
station_stats_sorted = station_stats.sort_values('range', ascending=False)
print("Top 5 stations by temperature range:")
print(station_stats_sorted.head())

# Find the maximum range value
max_range = station_stats['range'].max()
print(f"Largest temperature range: {max_range:.2f}°C")

# Find all stations that have this maximum range (handle potential ties)
largest_range_stations = station_stats[station_stats['range'] == max_range]
print(f"\nNumber of stations with largest range: {len(largest_range_stations)}")
print("\nStation(s) with largest temperature range:")
print(largest_range_stations)

# Save results to the required output file
with open("largest_temp_range_station.txt", "w") as f:
    for station_name, row in largest_range_stations.iterrows():
        min_temp = row['min']
        max_temp = row['max'] 
        range_temp = row['range']
        f.write(f"Station {station_name}: Range {range_temp:.1f}°C (Max: {max_temp:.1f}°C, Min: {min_temp:.1f}°C)\n")

print("Results saved to largest_temp_range_station.txt")