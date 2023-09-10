import streamlit as st
import pandas as pd
import plotly.express as px

def create_info_section(title, info_text):
    with st.expander(f"{title} - Know More?"):
        st.info(info_text)


orcidxofs_data = pd.read_csv('orcidxofs_2.csv')
unique_institutes = pd.read_csv('unique_institutes.csv')

st.sidebar.title('Select Institute')
institute_list = ['All'] + sorted(unique_institutes['unique_institute'].tolist())
selected_institute = st.sidebar.selectbox('Type or Select an Institute', institute_list)
st.sidebar.info("This dashboard holds information pertaining to the data sourced from OSF.")

if selected_institute == 'All':
    filtered_data = orcidxofs_data  
    
else:
    filtered_data = orcidxofs_data[orcidxofs_data['institute'] == selected_institute]

# filtered_data["date"] = pd.to_numeric(filtered_data["date"], errors="coerce")
# filtered_data = filtered_data[(filtered_data["date"] <= 2022) & (filtered_data["date"] >= 1930)]

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

st.markdown("---")

if not filtered_data_valid_dates.empty:
    date_counts = filtered_data_valid_dates['date'].value_counts().reset_index()
    date_counts.columns = ['Date', 'Frequency']
    date_counts = date_counts.sort_values(by='Date')
    fig = px.scatter(date_counts, x='Date', y='Frequency', labels={'Frequency': 'Frequency Count'}, title="Date Frequency Scatter Plot (Excluding 'none' Dates)")
    st.plotly_chart(fig)
else:
    st.info("No data with valid dates to plot.")


st.markdown("---")

modified_df = pd.read_csv("facInfo.csv")
unibe_df = pd.read_csv("unibe_data.csv")

merged_df = pd.merge(modified_df, unibe_df, on="institute", how="left")
merged_df.dropna(subset=["faculty"], inplace=True)


faculty_sum = merged_df.groupby('faculty')[['open', 'closed']].sum()
faculty_sum['oar'] = faculty_sum['open'] / (faculty_sum['open'] + faculty_sum['closed'])
faculty_sum['oar'] = faculty_sum['oar'].round(2)  # Round to two decimal places
faculty_sum = faculty_sum.sort_values(by='oar', ascending=False)
faculty_sum.reset_index(inplace=True)
faculty_sum_filtered = faculty_sum[faculty_sum['oar'] > 0]

fig = px.bar(faculty_sum_filtered, x='faculty', y='oar', labels={'faculty': 'Faculty', 'oar': 'OAR'})
fig.update_layout(
    title='Open Access Rate (OAR) by Faculty (Excluding OAR = 0)',
    xaxis_title='Faculty',
    yaxis_title='OAR',
)
st.plotly_chart(fig)

# Create info button and section for Open Access Ratio by Faculty
info_text_oar_faculty = "Open Access Ratio (OAR) by Faculty shows the open access publication rate for each faculty."
create_info_section("Open Access Ratio by Faculty", info_text_oar_faculty)


