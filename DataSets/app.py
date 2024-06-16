import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from prophet import Prophet


st.title("Data Analysis Portal")

# Informative Note about Data Cleaning
st.markdown("""
### Important Note:
Before uploading your dataset, please ensure that it has undergone necessary data cleaning and preprocessing steps. This includes handling missing values, removing duplicates, and ensuring that data types are correctly formatted. Clean and well-preprocessed data will lead to more accurate and meaningful analysis results.
""")

# File upload
uploaded_file = st.file_uploader("Upload your dataset (Excel or CSV)", type=['csv', 'xlsx'])
if uploaded_file:
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('csv') else pd.read_excel(uploaded_file)
    st.write("Dataset Preview:")
    st.dataframe(df.head())

    # Extract numeric columns
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_columns = df.select_dtypes(include=[object, 'category']).columns.tolist()


    # Basic stats and correlations
    if st.checkbox("Show basic statistics"):
        st.write(df.describe())

    if st.checkbox("Show correlation heatmap"):
        # Select only numeric columns for correlation
        numeric_df = df.select_dtypes(include=[np.number])
        corr = numeric_df.corr()
        plt.figure(figsize=(10, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm')
        st.pyplot(plt)

    # Filtering options
    if st.checkbox("Filter data"):
        filter_column = st.selectbox("Select column to filter", df.columns)
        unique_values = df[filter_column].unique()
        selected_values = st.multiselect("Select values", unique_values)
        if selected_values:
            df = df[df[filter_column].isin(selected_values)]
            st.write("Filtered Data Preview:")
            st.dataframe(df.head())

    # Data Visualization
    st.subheader("Data Visualization")

    # Histogram and Density Plots
    if st.checkbox("Show histogram and density plots"):
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        column = st.selectbox("Select column for histogram and density plot", numeric_columns)
        plt.figure(figsize=(10, 6))
        sns.histplot(df[column], kde=True)
        st.pyplot(plt)

    # Box Plots
    if st.checkbox("Show box plot"):
        column = st.selectbox("Select column for box plot", numeric_columns)
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=df[column])
        st.pyplot(plt)

    # Scatter Plots with Regression Lines
    if st.checkbox("Show scatter plot with regression line"):
        columns = st.multiselect("Select columns for scatter plot", numeric_columns, default=numeric_columns[:2])
        if len(columns) == 2:
            plt.figure(figsize=(10, 6))
            sns.regplot(x=df[columns[0]], y=df[columns[1]])
            st.pyplot(plt)
        else:
            st.error("Please select exactly two columns.")

    # Pair Plots
    if st.checkbox("Show pair plot"):
        selected_columns = st.multiselect("Select columns for pair plot", numeric_columns, default=numeric_columns[:5])
        if len(selected_columns) > 1:
            plt.figure(figsize=(10, 6))
            sns.pairplot(df[selected_columns])
            st.pyplot(plt)
        else:
            st.error("Please select at least two columns.")

    # Pie Chart
    if st.checkbox("Show pie chart"):
        column = st.selectbox("Select column for pie chart", categorical_columns)
        pie_data = df[column].value_counts().reset_index()
        pie_data.columns = [column, 'count']
        fig = px.pie(pie_data, names=column, values='count', title=f'Pie Chart of {column}')
        st.plotly_chart(fig)


# 3D Scatter Plots
    st.subheader("3D Scatter Plots")
    st.markdown("**Useful for visualizing relationships between three variables.**")
    if st.checkbox("Show 3D scatter plot"):
        columns = st.multiselect("Select columns for 3D scatter plot", numeric_columns, default=numeric_columns[:3])
        if len(columns) == 3:
            fig = px.scatter_3d(df, x=columns[0], y=columns[1], z=columns[2], title="3D Scatter Plot")
            st.plotly_chart(fig)
        else:
            st.error("Please select exactly three columns.")

    # Bar Charts for Categorical Data
    st.subheader("Bar Charts for Categorical Data")
    if st.checkbox("Show bar chart"):
        column = st.selectbox("Select column for bar chart", categorical_columns)
        bar_data = df[column].value_counts().reset_index()
        bar_data.columns = [column, 'count']
        fig = px.bar(bar_data, x=column, y='count', title=f'Bar Chart of {column}')
        st.plotly_chart(fig)

# To run the Streamlit app, use the command:
# streamlit run app.py
