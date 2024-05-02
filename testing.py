import streamlit as st
import pandas as pd

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

filtered_df = base_curves.iloc[:, :5]

final_df = optimise_curve(filtered_df, weeks = 10, budget = 10000000)