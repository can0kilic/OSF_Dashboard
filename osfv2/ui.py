import streamlit as st
import pandas as pd
import plotly.express as px

orcidxofs_data = pd.read_csv('orcidxofs_2.csv')
unique_institutes = pd.read_csv('unique_institutes.csv')

st.sidebar.title('Select Institute')
institute_list = ['All'] + unique_institutes['unique_institute'].tolist() 
selected_institute = st.sidebar.selectbox('Choose an institute', institute_list)
st.sidebar.info("This dashboard holds information pertaining to the data sourced from OSF.")

if selected_institute == 'All':
    filtered_data = orcidxofs_data  
    
else:
    filtered_data = orcidxofs_data[orcidxofs_data['institute'] == selected_institute]


st.title("OSF Dashboard")

st.success(f"Showing data for institute: {selected_institute}")
public_dict = {}
private_dict = {}

for index, row in filtered_data.iterrows():
    orcid = row['orcid']
    institute = row['institute']
    public = row['public']
    private = row['private']
    
    if orcid not in public_dict:
        public_dict[f"{orcid} {institute}"] = public
    if orcid not in private_dict:
        private_dict[f"{orcid} {institute}"] = private
   


public_rec = sum(list(public_dict.values()))
private_rec = sum(list(private_dict.values()))
total_rec = public_rec + private_rec

if total_rec > 0:
    oar = public_rec / total_rec
else:
    oar = 0.0

st.markdown("---")

col1, col2, col3, col5 = st.columns(4)
col1.metric("Open Access Rate", f"{oar:.2%}")
col2.metric("Open Entries", public_rec)
col3.metric("Closed Entries", private_rec)
col5.metric("Total Entries", total_rec)

st.markdown("---")

st.dataframe(filtered_data)

filtered_data_valid_dates = filtered_data[filtered_data['date'] != 'none']

if not filtered_data_valid_dates.empty:
    date_counts = filtered_data_valid_dates['date'].value_counts().reset_index()
    date_counts.columns = ['Date', 'Frequency']

    fig = px.scatter(date_counts, x='Date', y='Frequency', labels={'Frequency': 'Frequency Count'}, title="Date Frequency Scatter Plot (Excluding 'none' Dates)")
    st.plotly_chart(fig)
else:
    st.info("No data with valid dates to plot.")

st.markdown('<a href="https://unibedashboard.netlify.app/" target="_self">Return to Dashboard</a>', unsafe_allow_html=True)
