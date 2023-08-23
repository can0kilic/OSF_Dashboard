import streamlit as st
import pandas as pd
from extract_from_osf import retrieve_user_info
import time
import os

def generate_csv(response_dict, institute=None, full_name=None, orcid=None, processed_name=None, des=None, email=None):
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
    if os.path.exists("out.csv"):
        try:
            existing_df = pd.read_csv("out.csv")
        except pd.errors.EmptyDataError:
            existing_df = pd.DataFrame()
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df
    combined_df.drop_duplicates(subset=["title"], inplace=True)
    combined_df.to_csv("out.csv", index=False)


st.title("Manual Search in Osf")

full_name = st.text_input("enter name")
institute = st.text_input("enter institute")

search_term = st.text_input("enter the osf of user")
search_button = st.button("Search")
if search_button:
    with st.spinner("fetching..."):
        res = retrieve_user_info(search_term)
        if res: 
            st.success("Data Fetched")
            st.json(res)

            add_button = st.button("Add this data into dataset")
            if add_button:
                osf_id = fetched_data["osf_id"]
                public = fetched_data["no_of_public_projects"]
                private_projects = fetched_data["no_of_private_projects"]
                institute = selected_data["institute"]


                generate_csv(fetched_data, institute=institute, full_name=full_name)
                st.success("added successfully")


        else:
            st.error("Unable to fetch data.")

