import streamlit as st
import pandas as pd
from extract_from_osf import retrieve_user_info
import time
import os


import pandas as pd
import os

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



#=======================================================================================================

csv_path = "userinfo.csv"
df = pd.read_csv(csv_path)

if "index" not in st.session_state:
    st.session_state.index = 0

st.title("Data Management App")

st.write("Auto-generating dataset")

index = st.session_state.index if "index" in st.session_state else 0
selected_data = df.loc[st.session_state.index, ["full_name", "processed_name", "orcid", "institute", "des", "email"]]

st.markdown("---")

col1,colx = st.columns([9,1])
col1.metric("Full Name", selected_data["full_name"])
col2,cola = st.columns([9,1])
col2.metric("Processed Name", selected_data["processed_name"])
col3,colb = st.columns([9,1])
col3.metric("ORCID:", selected_data["orcid"])
col5,coly = st.columns([9,1])
col5.metric("Institute" , selected_data["institute"])

st.markdown("---")

with st.spinner('Wait for it...'):

    fetched_data = retrieve_user_info(selected_data["processed_name"], orcid=selected_data["orcid"])


if fetched_data is None:

    st.error("No Data Found!")
else:
    st.success("Data Fetched")
    osf_url = f"https://osf.io/{fetched_data['osf_id']}/"
    st.markdown(f"[Open OSF Link]({osf_url})")

    st.json(fetched_data)
    
    add_button = st.button("Add Data")
    if add_button:
        
        osf_id = fetched_data["osf_id"]
        public = fetched_data["no_of_public_projects"]
        private_projects = fetched_data["no_of_private_projects"]
        institute = selected_data["institute"]
        full_name = selected_data["full_name"]
        orcid = selected_data["orcid"]
        processed_name = selected_data["processed_name"]
        des = selected_data["des"]
        email = selected_data["email"]

        generate_csv(fetched_data, institute=institute, full_name=full_name, orcid=orcid, processed_name=processed_name, des=des, email=email)
       

    
        
next_button = st.button("Next")
if next_button:
    st.session_state.index = (st.session_state.index + 1) % len(df)
    


