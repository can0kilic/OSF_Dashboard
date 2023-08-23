import pandas as pd

def extract_unique_institutes(input_file, output_file):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_file)

    # Extract unique institute names from the 'institute' column
    unique_institutes = df['institute'].unique()
 
    # Create a new DataFrame with a single column for unique institute names
    institute_df = pd.DataFrame({'unique_institute': unique_institutes})

    # Write the new DataFrame to a new CSV file
    institute_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    input_file = "orcidxofs_2.csv"
    output_file = "unique_institutes.csv"

    extract_unique_institutes(input_file, output_file)
