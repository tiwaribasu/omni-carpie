import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def get_data(file):
    df = pd.read_excel(file)
    df['Dates'] = pd.to_datetime(df['Dates'], dayfirst=True)
    df['Dates'] = df['Dates'].dt.strftime('%d-%m-%Y')

    # Options Data
    df_option = df.loc[:, :'Equity Portfolio'].drop('Equity Portfolio', axis=1)
    df_option.columns = df_option.iloc[0]
    df_option = df_option.iloc[1:]
    df_option.reset_index(drop=True, inplace=True)
    df_option = df_option.rename(columns={df_option.columns[0]: 'Date'})

    # Equity Data
    df_equity = pd.concat([df[['Dates']], df.loc[:, 'Equity Portfolio':]], axis=1)
    df_equity.columns = df_equity.iloc[0]
    df_equity = df_equity.iloc[1:]
    df_equity.reset_index(drop=True, inplace=True)
    df_equity = df_equity.rename(columns={df_equity.columns[0]: 'Date'})

    return df_option, df_equity


def main():
    # Load Results Data
    file = 'Dashboard.xlsx'
    df_option, df_equity = get_data(file)

    # Selections
    portfolio = st.sidebar.selectbox('Portfolio Type', ('Equity', 'Options'))
    if portfolio == 'Equity':
        df = df_equity
    elif portfolio == 'Options':
        df = df_option

    # Show Results Data
    st.write(df)

    # Plots
    column_headers = df.columns[1:]
    column_headers_with_all = ['All'] + list(column_headers)
    column_to_plot = st.sidebar.selectbox('Select column to plot', column_headers_with_all)

    plt.figure(figsize=(10, 6))
    if column_to_plot == 'All':
        for column in column_headers:
            plt.plot(df['Date'].values, df[column].values, label=column)
    else:
        plt.plot(df['Date'].values, df[column_to_plot].values)

    # Labels and Title
    plt.xlabel('Date')
    plt.ylabel('P&L')
    plt.title('P&L Over Time')
    plt.legend()

    plt.xticks(rotation=45)

    # Displaying Plot
    st.pyplot(plt.gcf())

if __name__ == "__main__":
    main()