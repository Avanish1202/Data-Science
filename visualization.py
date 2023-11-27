import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Suppressing the deprecation warning
st.set_option('deprecation.showPyplotGlobalUse', False)

def main():
    st.title("Seaborn Data Visualization App")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

    if uploaded_file is not None:
        # Read the data
        data = pd.read_csv(uploaded_file)

        # Display the dataset
        st.subheader("Dataset")
        st.dataframe(data)

        # Select x-axis column
        x_column = st.selectbox("Select X-Axis Column", data.columns, key="x_column_selectbox")

        # Select y-axis column
        y_column = st.selectbox("Select Y-Axis Column", data.columns, key="y_column_selectbox")

        # Select Seaborn plot type
        plot_type = st.selectbox("Select Seaborn Plot Type", get_seaborn_plot_types(), key="plot_type_selectbox")

        # Generate Seaborn plot
        generate_seaborn_plot(data, x_column, y_column, plot_type)

def get_seaborn_plot_types():
    return [
        "Scatter Plot", "Line Plot", "Bar Plot", "Count Plot",
        "Box Plot", "Violin Plot", "Strip Plot", "Swarm Plot",
        "Heatmap", "Pair Plot", "Histogram", "Bar Graph", "Pie Chart"
    ]

def generate_seaborn_plot(data, x_column, y_column, plot_type):
    st.subheader(f"{plot_type} - {x_column} vs {y_column}")

    try:
        if plot_type == "Scatter Plot":
            sns.scatterplot(x=x_column, y=y_column, data=data, hue=y_column)
            st.pyplot()
        elif plot_type == "Line Plot":
            sns.lineplot(x=x_column, y=y_column, data=data, hue=y_column)
            st.pyplot()
        elif plot_type == "Bar Plot":
            sns.barplot(x=x_column, y=y_column, data=data, hue=y_column)
            st.pyplot()
        elif plot_type == "Count Plot":
            sns.countplot(x=x_column, data=data, hue=y_column)
            st.pyplot()
        elif plot_type == "Box Plot":
            sns.boxplot(x=x_column, y=y_column, data=data, hue=y_column)
            st.pyplot()
        elif plot_type == "Violin Plot":
            sns.violinplot(x=x_column, y=y_column, data=data, hue=y_column)
            st.pyplot()
        elif plot_type == "Strip Plot":
            sns.stripplot(x=x_column, y=y_column, data=data, hue=y_column, jitter=True)
            st.pyplot()
        elif plot_type == "Swarm Plot":
            sns.swarmplot(x=x_column, y=y_column, data=data, hue=y_column)
            st.pyplot()
        elif plot_type == "Heatmap":
            st.warning("Heatmap visualization requires a matrix-like dataset. Please select appropriate columns.")
            st.warning("Displaying correlation heatmap for selected columns.")
            heatmap_data = data[[x_column, y_column]].corr()
            sns.heatmap(heatmap_data, annot=True, cmap='coolwarm')
            st.pyplot()
        elif plot_type == "Pair Plot":
            st.warning("Pair Plot visualization is not supported in Streamlit. Choose another plot type.")
        elif plot_type == "Histogram":
            plt.hist(data[x_column])
            st.pyplot()
        elif plot_type == "Bar Graph":
            data[x_column].value_counts().plot(kind='bar')
            st.pyplot()
        elif plot_type == "Pie Chart":
            st.warning("Pie Chart visualization requires a single categorical column. Please select an appropriate column.")
            pie_data = data[x_column].value_counts()
            plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=140)
            st.pyplot()

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
