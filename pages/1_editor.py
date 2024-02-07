import streamlit as st
import pandas as pd
from st_files_connection import FilesConnection
import gcsfs as gcsfs
# Create connection object and retrieve file contents.
conn = st.connection('gcs', type=FilesConnection)

df = pd.DataFrame()
edited_df = pd.DataFrame()
if "df" not in st.session_state:
    # st.session_state.df = pd.read_csv("data.csv",index_col=False)
    st.session_state.df = conn.read("birdsandweighbucket/data.csv",index_col=False, input_format="csv")
st.session_state.df['Date & Time'] = pd.to_datetime(st.session_state.df['Date & Time']) ##FIX FORMAT

# Function to save the DataFrame to a CSV file
def save_to_csv(dfToSave):
    if not dfToSave.empty:
        # dfToSave.to_csv("data.csv", index=False, encoding="utf-8") #Save local csv
        conn.open("birdsandweighbucket/data.csv",index_col=False, input_format="csv", ttl=600)
        with conn.open("birdsandweighbucket/data.csv", "wt") as f:
            dfToSave.to_csv(f, index=False)
    st.warning("Edited data saved to data.csv")
def refresh():
    # st.session_state.df = conn.read("birdsandweighbucket/data.csv",index_col=False, input_format="csv")
    st.session_state.df = pd.read_csv("data.csv",index_col=False)

edited_df = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True)
# Button to save the edited data to a CSV file
if st.button(label="Save data_editor to CSV", type="primary"):
    save_to_csv(edited_df)
    refresh()
    st.rerun()