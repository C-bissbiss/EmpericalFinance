import csv
import pandas as pd

file_path = "ks-projects-201801.csv"

def parse_malformed_row(row):
    try:
        # Attempt to parse the row as a regular CSV row
        parsed_row = next(csv.reader([row]))
        if len(parsed_row) != expected_columns:
            # If the parsed row doesn't have the expected number of columns, return None
            return None
        return parsed_row
    except:
        # In case of any error during parsing, return None
        return None

# Function to clean up the specific issues in the DataFrame
def clean_up_dataframe(df):
    # Remove all " characters
    df = df.replace('"', '', regex=True)

    # Remove extra semicolons in 'usd_goal_real' column
    if 'usd_goal_real;;;;' in df.columns:
        df['usd_goal_real'] = df['usd_goal_real;;;;'].str.replace(';;;;', '', regex=False)
        df.drop(columns=['usd_goal_real;;;;'], inplace=True)

    return df

# Read the CSV file and process it
with open(file_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    header = next(reader)  # Get the header row
    expected_columns = len(header)  # Expected number of columns

    regular_data = []  # To store correctly formatted rows
    special_data = []  # To store specially parsed rows

    for row in reader:
        if len(row) == expected_columns:
            # Row is correctly formatted
            regular_data.append(row)
        else:
            # Try to parse malformed row
            parsed_row = parse_malformed_row(','.join(row))
            if parsed_row:
                special_data.append(parsed_row)

# Convert the lists to DataFrames
df_regular = pd.DataFrame(regular_data, columns=header)
df_special = pd.DataFrame(special_data, columns=header)

# Combine the DataFrames
df_combined = pd.concat([df_regular, df_special], ignore_index=True)

# Cleaning up the DataFrame
df_cleaned = clean_up_dataframe(df_combined)

output_file_path = 'ks-projects-201801-cleaned.csv'

df_cleaned.to_csv(output_file_path, index=False)