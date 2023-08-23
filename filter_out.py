import pandas as pd
from datetime import datetime

def process_csv(input_file, output_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_file)

    # Remove duplicate rows based on all columns
    df.drop_duplicates(inplace=True)

    # Remove rows where both public and private columns are 0
    df = df[~((df['public'] == 0) & (df['private'] == 0))]

    # Save the intermediate DataFrame to a temporary CSV file
    temp_file = "temp.csv"
    df.to_csv(temp_file, index=False)

    # Read the temporary CSV file into a new DataFrame
    df_temp = pd.read_csv(temp_file)

    # Convert the last column containing list of tuples to individual columns
    df_temp['list_of_work'] = df_temp['list_of_work'].apply(eval)

    # Create a new DataFrame by expanding rows for each element in the 'list_of_work' column
    df_expanded = df_temp.explode('list_of_work')

    # Split the tuples in 'list_of_work' column into separate columns
    df_expanded[['title', 'date']] = pd.DataFrame(df_expanded['list_of_work'].tolist(), index=df_expanded.index)

    # Drop the original 'list_of_work' column
    df_expanded.drop(columns=['list_of_work'], inplace=True)

    # If the length of the list is 0, replace 'date' and 'title' with 'none'
    df_expanded['date'].fillna('none', inplace=True)
    df_expanded['title'].fillna('none', inplace=True)

    # Convert dates to year format "YYYY" if date is not 'none'
    df_expanded.loc[df_expanded['date'] != 'none', 'date'] = df_expanded.loc[df_expanded['date'] != 'none', 'date'].apply(lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%f").year)

    # Save the processed DataFrame to the final CSV file
    df_expanded.to_csv(output_file, index=False)

if __name__ == "__main__":
    input_csv = "out.csv"
    output_csv = "orcidxofs_2.csv"

    # Process CSV and generate the final CSV
    process_csv(input_csv, output_csv)
