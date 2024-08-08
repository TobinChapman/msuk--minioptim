# import streamlit as st
# import numpy as np


# import streamlit as st
# import pandas as pd
# import numpy as np

# tab = st.sidebar.selectbox("Tabs", ["📈 Chart", "🗃 Data"])
# data = np.random.randn(10, 1)

# base_curves = pd.DataFrame(pd.read_csv('all_kfc_curves.csv'))

# curves_only = base_curves.drop('netspend',axis=1)

# if tab == "📈 Chart":
#     st.subheader("A tab with a chart")
#     st.line_chart(data)

# elif tab == "🗃 Data":
#     st.title("Optimise Budget Across ")

#     option = st.multiselect('Select your Campaigns:', curves_only.columns.tolist()) 

#     # Create a sample dataframe
#     data = {'Column1': ['Value1', 'Value2'], 'Column2': ['Value3', 'Value4']}
#     df = pd.DataFrame(data)

#     # Display the dataframe
#     st.write(df)

#     # Create input fields for each cell
#     for i in range(len(df)):
#         for j in range(len(df.columns)):
#             df.iloc[i, j] = st.text_input(f'Row {i+1} Column {j+1}', df.iloc[i, j])

#     # Display the updated dataframe
#     st.write(df)

import streamlit as st
import pandas as pd
import numpy as np

tab = st.sidebar.selectbox("Tabs", ["📈 Chart", "🗃 Data"])
data = np.random.randn(10, 1)

base_curves = pd.DataFrame(pd.read_csv('all_kfc_curves.csv'))

curves_only = base_curves.drop('netspend',axis=1)

if tab == "📈 Chart":
    st.subheader("A tab with a chart")
    st.line_chart(data)

elif tab == "🗃 Data":
    st.title("Optimise Budget Across ")

    options = st.multiselect('Select your Campaigns:', curves_only.columns.tolist()) 

    # Create a dictionary to store the inputs
    inputs = {}

    # Create input fields for each selected option
    for i, option in enumerate(options):
        inputs[option] = st.text_input(f'Input for {option}')

    # Display the inputs
    st.write(inputs)