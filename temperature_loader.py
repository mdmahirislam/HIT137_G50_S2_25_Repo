import os
import pandas as pd
    
# Load list of CSV file paths
def load_temperature_data(folder_path):
    if os.path.exists(folder_path):
        print(f"Folder '{folder_path}' found!")
        #Finding the csv files
        csv_files = []
        for filename in os.listdir(folder_path):
            if filename.endswith('.csv'):
                full_path = os.path.join(folder_path, filename)
                csv_files.append(full_path)

        print(f"Found {len(csv_files)} CSV files: {csv_files}")
        return csv_files
    else:
        print(f"Folder '{folder_path}' not found!")
        return []

# Process a single CSV file into long format       
def process_file(file_path):
    df = pd.read_csv(file_path)


    # Reshape months from horizontal to vertical orientation
    df_long = df.melt(
        id_vars=["STATION_NAME", "STN_ID", "LAT", "LON"],
        value_vars=["January", "February", "March", "April", "May", "June", 
                    "July", "August", "September", "October", "November", "December"],
        var_name="Month",
        value_name="Temperature"
    )

    # Map month names → numbers
    month_map = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12
    }
    df_long["Month_Num"] = df_long["Month"].map(month_map)
      
    # Extract year from filename
    import re 
    file_name = os.path.basename(file_path)
    match = re.search(r"(\d{4})", file_name)
    year = int(match.group(1)) if match else None
    df_long["Year"] = year
    
    return df_long
    
# Combine all CSVs into one DataFrame
def get_combined_data(folder_path="temperatures"):
    csv_files = load_temperature_data(folder_path)
    all_dfs = [process_file(file) for file in csv_files]
    combined_df = pd.concat(all_dfs, ignore_index=True)
    return combined_df

if __name__ == "__main__":
    combined_df = get_combined_data("temperatures")
    print("Combined shape:", combined_df.shape)
    print(combined_df.head(15))


