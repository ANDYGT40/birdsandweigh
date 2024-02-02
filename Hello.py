import streamlit as st
import pandas as pd
# import plotly.express as px
from datetime import datetime
from st_files_connection import FilesConnection
# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.connection('gcs', type=FilesConnection)

#Setup:
# Get today's date & time
date = datetime.now()
dt_iso = date.isoformat()
dt_string = date.strftime("%Y-%m-%d %H:%M:%S")
t_string = date.strftime("%H:%M")
d_string = date.strftime("%d-%m-%Y")
# df = pd.DataFrame.empty
# Get data from csv
df = pd.DataFrame()
edited_df = pd.DataFrame()
if "df" not in st.session_state:
    # st.session_state.df = pd.read_csv("data.csv",index_col=False)
    st.session_state.df = conn.read("birdsandweighbucket/data.csv",index_col=False, input_format="csv", ttl=600)
st.session_state.df['Date & Time'] = pd.to_datetime(st.session_state.df['Date & Time']) ##FIX FORMAT



#Functions:
# Function to add a new row to the DataFrame
def addRow(date, field1, field2, oldTable):
    newRow = pd.DataFrame([[date, field1, field2]], columns=["Date & Time", "BB", "Bowie"])
    st.session_state.df = pd.concat([oldTable, newRow], ignore_index=True)
    st.session_state.df['Date & Time'] = pd.to_datetime(st.session_state.df['Date & Time']) 

# Function to save the DataFrame to a CSV file
def save_to_csv(dfToSave):
    if not dfToSave.empty:
        dfToSave.to_csv("data.csv", index=False, encoding="utf-8")
        st.warning("Data saved to data.csv")
    # Display a link to download the CSV file
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='data.csv',
            mime='text/csv',
        )
    else:
        st.warning('DataFrame Empty!')
        

def display_plot(data):
    # fig = px.line(data, x="Date & Time", y=["BB", "Bowie"], range_y=[0, 100])
    # st.plotly_chart(fig)
    st.line_chart(data, x="Date & Time", y=["BB", "Bowie"])

st.title(":hatched_chick: Birds&Weigh :baby_chick:")

#Containers
col1, col2 = st.columns(2)
#Display
with col1:
    st.write("### Data Input")
    with st.form("addRow_form"):
        date = st.text_input("Date & Time", value=dt_string)
        field1 = st.number_input("BB")
        field2 = st.number_input("Bowie")
        submitButton = st.form_submit_button("Add Row")
        deleteButton = st.form_submit_button("Delete last row")
    if submitButton:# # Add fields to data table and display the added fields
        addRow(date, field1, field2, st.session_state.df)
        st.warning(f"BB = {field1}g and Bowie = {field2}g. Submitted on {d_string} table at {t_string}")
    if deleteButton:
        st.warning(f"Row {st.session_state.df.index[-1]} dropped from dataset: ")
        st.session_state.df = st.session_state.df.drop(st.session_state.df.index[-1])
# Button to save the edited data to a CSV file
    if st.button(label="Save to CSV", type="primary"):
        save_to_csv(st.session_state.df)

# st.write(f"BB = {field1}g and Bowie = {field2}g. Submitted on {d_string} table at {t_string}")
with col2:
    st.write("### Data Table")
    st.write(f"{len(st.session_state.df)} total rows. Showing last 7 entries") #number of data rows
    st.write(f"Today's date: {d_string}")
    st.dataframe(st.session_state.df[-7:])
    maxBB = st.session_state.df.max()["BB"]
    maxBowie = st.session_state.df.max()["Bowie"]
    st.write(f"Max weight BB:{maxBB}, Bowie:{maxBowie}")


#Below columns
st.write("### All Measurements")
display_plot(st.session_state.df)
#st.write(st.session_state.df.dtypes) #Check Types

#split data into morning and night
ts = st.session_state.df.set_index('Date & Time')
#st.write(ts.dtypes) #Check Types
morn = ts.between_time('0:00','12:00')
night = ts.between_time('12:00','23:00')
st.write("### Morning")
maxMornBB = morn.max()["BB"]
maxMornBowie = morn.max()["Bowie"]
st.write(f"Max morning weight BB:{maxMornBB}, Bowie:{maxMornBowie}")
st.line_chart(morn,y=["BB", "Bowie"])
st.write("### Night")
maxNightBB = night.max()["BB"]
maxNightBowie = night.max()["Bowie"]
st.write(f"Max night weight BB:{maxNightBB}, Bowie:{maxNightBowie}")
st.line_chart(night,y=["BB", "Bowie"])

with st.expander("### Full Dataset (EDITABLE) **not working"):
    st.data_editor(st.session_state.df, num_rows="dynamic")

#####
# Features to add:
#   Connect to google sheets
#   Display warning if consecutive measurements are dropping 
#   Calculate and show trend
#   Full editable dataset (hidden) 