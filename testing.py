import streamlit as st
import pandas as pd

# Assuming you have a DataFrame 'df'
df = pd.read_csv('all_kfc_curves.csv')

# Create a multiselect widget for the y-axis
y_options = [col for col in df.columns if df[col].dtype in ['int64', 'float64']]
selected_y_columns = st.multiselect('Select columns to plot', y_options)

if selected_y_columns:
    # Create a new DataFrame with the selected columns
    plot_df = df[selected_y_columns]

    # Plot the line chart
    st.line_chart(plot_df)
else:
    st.write("Please select at least one column to plot.")