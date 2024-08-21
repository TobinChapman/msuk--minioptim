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

#     options = st.multiselect('Select your Campaigns:', curves_only.columns.tolist()) 

#     # Create a dictionary to store the inputs
#     inputs = {}

#     # Create input fields for each selected option
#     for i, option in enumerate(options):
#         inputs[option] = st.text_input(f'Input for {option}')

#     # Display the inputs
#     st.write(inputs)


#==============================================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

base_curves = pd.DataFrame(pd.read_csv('all_kfc_curves.csv'))

curves_only = base_curves.drop('netspend',axis=1)

def optimise_curve(df, budget, weeks):
    steps = budget/weeks/1000
    
    # Calculate increments and select top steps
    increments = df.diff().fillna(0).melt(var_name='Campaign', value_name='value')
    top_increments = increments.nlargest(round(steps), 'value')
    
    # Count occurrences and calculate budget allocation
    budget_df = top_increments['Campaign'].value_counts().reset_index()
    budget_df.columns = ['Campaign', 'count']
    budget_df['Campaign'] = budget_df['Campaign'].str.replace('_incr', '')
    
    # Calculate budgets and weekly budgets
    total_count = budget_df['count'].sum()
    budget_df['Budget'] = (budget_df['count'] / total_count * budget).round()
    budget_df['wklybudget'] = (budget_df['Budget'] / weeks).round(-3)
    
    # Calculate predictions
    budget_df['Predicted_Transactions'] = (budget_df.apply(lambda row: base_curves.loc[row['wklybudget'], row['Campaign']], axis=1) * weeks).round()
    budget_df['Predicted_Revenue'] = (budget_df['Predicted_Transactions'] * 13.13).round()
    
    # Add total row
    total_row = budget_df.sum().to_frame().T
    total_row['Campaign'] = 'Total'
    budget_df = pd.concat([budget_df, total_row], ignore_index=True)
    
    # Calculate ROI and drop unnecessary columns
    budget_df['Predicted_ROI'] = (budget_df['Predicted_Revenue'] / budget_df['Budget']).round(1)
    budget_df = budget_df.drop(['count', 'wklybudget'], axis=1)
    
    return budget_df


def main():
    st.set_page_config(page_title="KFC Optimiser", page_icon=":dart:", initial_sidebar_state="expanded")
    st.image('kfc_logo.PNG', width=150)
    st.title("Optimise Budget Across Campaigns")
    st.write("Input budget and number of weeks the media is running. Then select your Campaigns:")

    weeks_in = st.number_input("Number of weeks", value=10, step=1, placeholder="Type a number...")
    budget_in = st.number_input("Total budget", value=10000000, step=10000, placeholder="Type a number...")
    option = st.multiselect('Select your Campaigns:', curves_only.columns.tolist()) 

    if weeks_in is not None and budget_in is not None and option:
        filtered_df = curves_only[option]
        final_df = optimise_curve(filtered_df, weeks = weeks_in, budget = budget_in)
        st.write(final_df)

        final_df_rmv = final_df.drop('Total', axis=0)
        plt.figure(figsize=(8, 8))
        plt.pie(final_df_rmv['Budget'], labels=final_df_rmv['Campaign'], autopct='%1.1f%%')
        plt.title('Budget Split')
        
        st.pyplot(plt)

        fig = go.Figure()
        chart_df = filtered_df.iloc[:400, :]
        for col in chart_df.columns:
            fig.add_trace(go.Scatter(x=chart_df.index, y=chart_df[col], mode='lines', name=col))

        fig.update_layout(
            autosize=False,
            width=800,
            height=500,
            xaxis_title="Netspend (£k)",
            yaxis_title="Revenue Generated (£)",
        )

        st.plotly_chart(fig)


    else:
        st.write("Please fill in all inputs and select at least one Campaign.")

if __name__ == '__main__':
    main()