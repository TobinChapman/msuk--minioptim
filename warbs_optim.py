import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

base_curves = pd.DataFrame(pd.read_csv('all_warbs_curves.csv'))

curves_only = base_curves.drop('netspend',axis=1)

def optimise_curve(df, budget, weeks):
    # create a new df to hold the results
    df_mid = pd.DataFrame()

    #calculate the number of 'units' that we have to assign
    units = budget/weeks/1000
    
    for col in df.columns:
        df_mid[col + '_incr'] = df[col].diff().fillna(0)
    
    df_mid = df_mid.filter(regex='_incr').melt(var_name = 'Campaign').nlargest(round(units), 'value')

    budget_df = pd.DataFrame(df_mid['Campaign'].value_counts()).reset_index()

    budget_df['Campaign'] = budget_df['Campaign'].str.replace('_incr', '')

    budget_df['Budget'] = (budget_df['count']/(budget_df['count'].sum()))*budget

    budget_df = budget_df.drop('count',axis=1)

    budget_df['Budget'] = budget_df['Budget'].round()

    budget_df['wklybudget'] = (budget_df['Budget']/weeks).round(-3)

    base_curves.set_index('netspend', inplace=True)

    budget_df['Predicted_Transactions'] = ((budget_df.apply(lambda row: base_curves.loc[row['wklybudget'], row['Campaign']], axis=1))*weeks).round()

    budget_df['Predicted_Revenue'] = (budget_df['Predicted_Transactions']*13.13).round()

    budget_df.loc['Total'] = budget_df.sum()

    budget_df.at['Total', 'Campaign'] = 'Total'

    budget_df['Predicted_ROI'] = (budget_df['Predicted_Revenue']/budget_df['Budget']).round(1)
    
    budget_df = budget_df.drop('wklybudget', axis=1)
    
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
