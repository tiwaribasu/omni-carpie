import streamlit as st
import pandas as pd

# Load the Excel file
excel_file = 'Daily_PnL.xlsx'

# Read all sheets into a dictionary of DataFrames
sheets_dict = pd.read_excel(excel_file, sheet_name=None)

# Function to clean and convert data to numeric
def clean_and_convert(df):
    for col in df.columns[1:]:
        df[col] = df[col].replace({',': ''}, regex=True).astype(float)
    return df

# Function to calculate the last 21D P&L, last 60D P&L, and Since Inception P&L
def calculate_pnl_metrics(df, col):
    today_pnl = df[col].iloc[-1]
    last_21d_pnl = df[col].iloc[-21:].sum()
    last_60d_pnl = df[col].iloc[-60:].sum()
    since_inception_pnl = df[col].sum()
    return today_pnl, last_21d_pnl, last_60d_pnl, since_inception_pnl

# Streamlit App
st.set_page_config(layout="wide")  # Set layout to wide for full screen

all_data = []

# Two Columns
col1, col2 = st.columns([3, 2])

# Sheetwise P&L metrics
with col1:
    for sheet_name, df in sheets_dict.items():
        st.header(f'{sheet_name} P&L')
        
        df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
        df = clean_and_convert(df)
        all_data.append(df)

        metrics = {'Name': [], "Today's P&L": [], 'Last 21D P&L': [], 'Last 60D P&L': [], 'Since Inception': []}

        for col in df.columns[1:]:
            today_pnl, last_21d_pnl, last_60d_pnl, since_inception_pnl = calculate_pnl_metrics(df, col)
            metrics['Name'].append(col)
            metrics["Today's P&L"].append(int(today_pnl))
            metrics['Last 21D P&L'].append(int(last_21d_pnl))
            metrics['Last 60D P&L'].append(int(last_60d_pnl))
            metrics['Since Inception'].append(int(since_inception_pnl))

        metrics_df = pd.DataFrame(metrics)
        metrics_df = metrics_df.set_index('Name')

        def color_negative_red(value):
            color = 'red' if value < 0 else 'green'
            return f'color: {color}'

        styled_df = metrics_df.style.applymap(color_negative_red).format("{:.2f}")
        st.table(styled_df)

# Concatenate all data for monthly P&L calculation
all_data_df = pd.concat(all_data)

# Calculate monthly P&L
all_data_df['Month'] = all_data_df['Date'].dt.to_period('M')

# Select only the numeric columns for aggregation
numeric_columns = all_data_df.select_dtypes(include='number').columns
monthly_pnl = all_data_df.groupby('Month')[numeric_columns].sum().reset_index()
monthly_pnl['Month'] = monthly_pnl['Month'].dt.strftime('%b, %Y')

# Display Monthly P&L on the right side
with col2:
    st.header('Monthly P&L')
    monthly_pnl = monthly_pnl.set_index('Month')
    def color_negative_red_monthly(value):
        color = 'red' if value < 0 else 'green'
        return f'color: {color}'

    styled_monthly_pnl = monthly_pnl.style.applymap(color_negative_red_monthly).format("{:.2f}")
    st.table(styled_monthly_pnl)
