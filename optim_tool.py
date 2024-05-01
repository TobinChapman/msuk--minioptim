import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

base_curves = pd.DataFrame(pd.read_csv('all_kfc_curves.csv'))

base_curves = base_curves.drop('netspend',axis=1)

def optimise_curve(df, budget, weeks):
    # create a new df to hold the results
    df_mid = pd.DataFrame()

    #calculate the number of 'units' that we have to assign
    units = budget/weeks/1000
    
    for col in df.columns:
        df_mid[col + '_incr'] = df[col].diff().fillna(0)
    
    df_mid = df_mid.filter(regex='_incr').melt(var_name = 'campaign').nlargest(round(units), 'value')

    budget_df = pd.DataFrame(df_mid['campaign'].value_counts()).reset_index()

    budget_df['campaign'] = budget_df['campaign'].str.replace('_incr', '')

    budget_df['budget'] = (budget_df['count']/(budget_df['count'].sum()))*budget

    budget_df = budget_df.drop('count',axis=1)

    budget_df['budget'] = budget_df['budget'].round()
    
    return budget_df

def main():
    st.set_page_config(page_title="KFC Optimiser", page_icon=":dart:", initial_sidebar_state="expanded")
    st.title("Optimise Budget Across Campaigns")
    st.write("Input budget and number of weeks the media is running. Then select your campaigns:")

    weeks_in = st.number_input("Number of weeks", value=10, step=1, placeholder="Type a number...")
    budget_in = st.number_input("Total budget", value=10000000, step=10000, placeholder="Type a number...")
    option = st.multiselect('Select your campaigns:', base_curves.columns.tolist()) 

    if weeks_in is not None and budget_in is not None and option:
        filtered_df = base_curves[option]
        final_df = optimise_curve(filtered_df, weeks = weeks_in, budget = budget_in)
        st.write(final_df)
    else:
        st.write("Please fill in all inputs and select at least one campaign.")

    
    if weeks_in is not None and budget_in is not None and option:
        plt.figure(figsize=(8, 8))
        plt.pie(final_df['budget'], labels=final_df['campaign'], autopct='%1.1f%%')
        plt.title('Budget Split')
        

        st.pyplot(plt)

    if weeks_in is not None and budget_in is not None and option:
        fig = go.Figure()

        for col in filtered_df.columns:
            fig.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df[col], mode='lines', name=col))

        fig.update_layout(
            autosize=False,
            width=800,
            height=500,
            xaxis_title="Netspend (£k)",
            yaxis_title="Revenue Generated (£)",
        )

        st.plotly_chart(fig)

        #st.pyplot(fig)

if __name__ == '__main__':
    main()
