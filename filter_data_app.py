import streamlit as st
import pandas as pd
import duckdb

# Function to load data from the Parquet file
@st.cache_data
def load_data():
    url = 'https://github.com/vkt1414/idc-index-data/releases/download/0.1/segmentation_completeness.parquet'
    query = f"SELECT * FROM '{url}'"
    return duckdb.query(query).to_df()

# Function to filter data based on user input
def filter_data(df, completeness, body_part, laterality):
    query = "SELECT * FROM df WHERE 1=1"
    if completeness:
        completeness_values = ','.join([f"'{item}'" for item in completeness])
        query += f" AND segmentation_completeness_check IN ({completeness_values})"
    if body_part:
        body_part_values = ','.join([f"'{item}'" for item in body_part])
        query += f" AND bodyPart IN ({body_part_values})"
    if laterality:
        laterality_values = ','.join([f"'{item}'" for item in laterality])
        query += f" AND laterality IN ({laterality_values})"
    return duckdb.query(query).to_df()

# Main function to run the Streamlit app
def main():
    st.title("Data Filtering App")
    st.write("Filter the data based on segmentation_completeness_check, bodyPart, and laterality.")

    # Load the data
    df = load_data()

    # Create widgets for filtering
    with st.sidebar:
        st.title("Filters")
        completeness_options = df['segmentation_completeness_check'].unique().tolist()
        body_part_options = df['bodyPart'].unique().tolist()
        laterality_options = df['laterality'].unique().tolist()

        completeness = st.multiselect("Select Segmentation Completeness", completeness_options)
        body_part = st.multiselect("Select Body Part", body_part_options)
        laterality = st.multiselect("Select Laterality", laterality_options)

    # Filter the data based on user input
    filtered_data = filter_data(df, completeness, body_part, laterality)

    # Display the filtered data
    st.header("Filtered Data")
    st.write("Number of Rows:", len(filtered_data))
    st.dataframe(filtered_data)

if __name__ == "__main__":
    main()
