import pandas as pd
import os
from extract_from_osf import retrieve_user_info

def generate_csv(response_dict, institute=None, full_name=None, orcid=None, processed_name=None, des=None, email=None):
    # Create a DataFrame with the new data
    data = []
    for title, date in response_dict.get("public_projects", []):
        data.append({
            "full_name": full_name,
            "des": des,
            "email": email,
            "institute": institute,
            "orcid": orcid,
            "processed_name": processed_name,
            "public": response_dict.get("no_of_public_projects"),
            "private": response_dict.get("no_of_private_projects"),
            "title": title,
            "date": str(date)[:4] if date else None,
            "osf_id": response_dict.get("osf_id")
        })

    # Check if the project list is empty, and if private projects exist
    if not response_dict.get("public_projects") and response_dict.get("no_of_private_projects", 0) > 0:
        data.append({
            "full_name": full_name,
            "des": des,
            "email": email,
            "institute": institute,
            "orcid": orcid,
            "processed_name": processed_name,
            "public": response_dict.get("no_of_public_projects"),
            "private": response_dict.get("no_of_private_projects"),
            "title": None,
            "date": None,
            "osf_id": response_dict.get("osf_id")
        })

    new_df = pd.DataFrame(data)
    
    # Read the existing CSV file (if it exists)
    if os.path.exists("out.csv"):
        try:
            existing_df = pd.read_csv("out.csv")
        except pd.errors.EmptyDataError:
            existing_df = pd.DataFrame()
        
        # Concatenate the new DataFrame with the existing DataFrame
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df
    
    # Remove duplicate titles
    combined_df.drop_duplicates(subset=["title"], inplace=True)
    
    # Save the combined DataFrame to the CSV file
    combined_df.to_csv("out.csv", index=False)

x = retrieve_user_info("j9n2y")
generate_csv(x,institute="xyz")

# Example usage
# response_dict = {
#     "no_of_public_projects": 0,
#     "no_of_private_projects": 1,
#     "osf_id": "123456",
#     "public_projects": []
# }
# generate_csv(response_dict, institute="Sample Institute", full_name="Jane Smith", orcid="1111-2222-3333-4444", processed_name="jane_smith", des="Scientist", email="jane.smith@example.com")

# response_dict = {
#     "no_of_public_projects": 4,
#     "no_of_private_projects": 2,
#     "osf_id": "12345622",
#     "public_projects": [
#         ("Project 4", "2022-09-25"),
#         ("Project 5", "2022-10-12"),
#         ("project 6", "1292")
        
#     ]
# }
# generate_csv(response_dict, institute="Sample Institute", full_name="Jane Smith", orcid="1111-2222-3333-4444", processed_name="jane_smith", des="Scientist", email="jane.smith@example.com")

