# Full code
import streamlit as st
import pandas as pd
import base64
from sklearn.preprocessing import StandardScaler

# Function to perform data cleaning
def clean_data(data, drop_columns, remove_null, fill_null, fill_value, data_types, column_filters,
               remove_duplicates, selected_columns_for_duplicates,
               remove_outliers, selected_columns_for_outliers, outlier_threshold,
               clean_text, selected_text_columns,
               feature_engineering, new_features,
               data_integrity_checks,
               scaling_normalization, numeric_columns,
               time_series_handling, timestamp_column):

    if drop_columns:
        data = data.drop(columns=drop_columns)

    if remove_null:
        data = data.dropna()

    if fill_null and fill_value is not None:
        data = data.fillna(fill_value)

    # Convert selected columns to specified data types
    for column, dtype in data_types.items():
        try:
            data[column] = data[column].astype(dtype)
        except KeyError as e:
            st.error(f"KeyError: {e}. Please check if '{column}' exists in the DataFrame.")

    # Apply column filters
    for column, values in column_filters.items():
        if values:
            data = data[data[column].astype(str).isin(values)]

    # Remove duplicate rows
    if remove_duplicates:
        data = data.drop_duplicates(subset=selected_columns_for_duplicates)

    # Remove outliers
    if remove_outliers:
        for column in selected_columns_for_outliers:
            data = data[(data[column] - data[column].mean()).abs() < outlier_threshold * data[column].std()]

    # Clean text columns
    if clean_text:
        for column in selected_text_columns:
            # You can add text cleaning processes here if needed
            pass

    # Feature engineering
    if feature_engineering:
        for feature in new_features:
            # Example: Creating a new feature by calculating the sum of two columns
            if len(feature.split(',')) == 2:
                col1, col2 = feature.split(',')
                data[f"{col1}_{col2}_sum"] = data[col1] + data[col2]
                st.success(f"New feature '{col1}_{col2}_sum' created successfully.")

    # Data integrity checks
    if data_integrity_checks:
        # Example: Check if the 'start_date' is earlier than the 'end_date'
        if 'start_date' in data.columns and 'end_date' in data.columns:
            date_inconsistencies = data[data['start_date'] > data['end_date']]
            if not date_inconsistencies.empty:
                st.warning("Data integrity check failed: 'start_date' should be earlier than 'end_date'")
                st.write(date_inconsistencies)
            if 'quantity' in data.columns:
                negative_quantities = data[data['quantity'] < 0]
                if not negative_quantities.empty:
                    st.warning("Data integrity check failed: 'quantity' should be non-negative")
                    st.write(negative_quantities)

    # Scaling and normalization
    if scaling_normalization:
        for column in numeric_columns:
            # Example: Standardize the values in the numeric column
            if column in data.columns:
                scaler = StandardScaler()
                data[column + '_standardized'] = scaler.fit_transform(data[[column]])
                st.success(f"Column '{column}' standardized successfully.")

    # Handling time series data
    if time_series_handling:
        # Example: Assuming you have a timestamp column named 'timestamp'
        if timestamp_column in data.columns:
            data[timestamp_column] = pd.to_datetime(data[timestamp_column])

            # Sort the DataFrame by the timestamp
            data.sort_values(by=timestamp_column, inplace=True)

            # Create lag features (e.g., lag 1, lag 2)
            for lag in range(1, 4):  # You can adjust the lag range as needed
                data[f'value_lag_{lag}'] = data['value'].shift(lag)

            st.success("Time series handling logic applied successfully.")

    return data

# Function to create a download link for the cleaned data
def create_download_link(df, filename="cleaned_data.csv"):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download Cleaned Data</a>'
    return href

# Streamlit app
def main():
    st.set_option('deprecation.showfileUploaderEncoding', False)
    st.set_option('deprecation.showPyplotGlobalUse', False)

    st.title("Data Cleaning App")

    # File upload
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        # Read data from the uploaded file with a different encoding
        data = pd.read_csv(uploaded_file, encoding='latin1')
        st.write("Data columns (total {} columns):".format(len(data.columns)))
        st.dataframe(data.dtypes.reset_index().rename(columns={0: 'Dtype', 'index': 'Column'}))

        # Display DataFrame summary
        st.write("DataFrame Summary:")
        st.dataframe(data.describe(include='all'))

        # Display the original data
        st.subheader("Original Data")
        st.dataframe(data)

        # User input for column removal
        selected_columns_to_remove = st.multiselect("Select columns to remove", data.columns)

        # User input for removing null values
        remove_null = st.checkbox("Remove rows with null values")

        # User input for filling null values
        fill_null = st.checkbox("Fill null values")

        fill_value = None
        if fill_null:
            fill_value = st.text_input("Enter the value to fill null values", "")

        # User input for changing column data types
        st.subheader("Change Column Data Types")

        # Create a dictionary to store selected column and data type
        data_types = {}
        for column in data.columns:
            # Use checkboxes to select multiple columns
            if st.checkbox(column):
                selected_dtype = st.selectbox(f"Select data type for {column}", ["", "int", "float", "str"])
                if selected_dtype:
                    data_types[column] = selected_dtype

        # User input for column filters
        st.subheader("Column Filters")

        # Create a multiselect box for selecting columns
        selected_columns = st.multiselect("Select columns for filtering", data.columns)

        # Create a dictionary to store selected column and filter values
        column_filters = {}
        for column in selected_columns:
            filter_values = st.text_input(f"Filter values for {column} (comma-separated)", "")
            if filter_values:
                column_filters[column] = [value.strip() for value in filter_values.split(',')]

        # User input for removing duplicate rows
        remove_duplicates = st.checkbox("Remove duplicate rows")

        # User input for selecting columns for duplicate removal
        selected_columns_for_duplicates = st.multiselect("Select columns for duplicate removal", data.columns)

        # User input for removing outliers
        remove_outliers = st.checkbox("Remove outliers")

        # User input for selecting columns for outlier removal
        selected_columns_for_outliers = st.multiselect("Select numeric columns for outlier removal",
                                                       data.select_dtypes('number').columns)

        # User input for outlier threshold
        outlier_threshold = st.number_input("Outlier threshold", value=3.0)

        # User input for text cleaning
        clean_text = st.checkbox("Clean text columns")

        # User input for selecting text columns
        selected_text_columns = st.multiselect("Select text columns for cleaning", data.select_dtypes('object').columns)

        # Button to trigger data cleaning and find null values
        if st.button("Clean Data and Find Null Values"):
            # Perform data cleaning
            data = clean_data(data, selected_columns_to_remove, remove_null, fill_null, fill_value, data_types,
                              column_filters,
                              remove_duplicates, selected_columns_for_duplicates,
                              remove_outliers, selected_columns_for_outliers, outlier_threshold,
                              clean_text, selected_text_columns,
                              feature_engineering=False,
                              new_features=[],
                              data_integrity_checks=False,
                              scaling_normalization=False,
                              numeric_columns=[],
                              time_series_handling=False,
                              timestamp_column=""
                              )

            # Display the cleaned data
            st.subheader("Cleaned Data")
            st.dataframe(data)

            # Display null values in the cleaned data
            st.subheader("Null Values in Cleaned Data")
            st.write(data.isnull().sum())

            # Create a download link for the cleaned data
            st.markdown(create_download_link(data), unsafe_allow_html=True)

if __name__ == "__main__":
    main()