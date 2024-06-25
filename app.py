import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt

st.set_page_config(layout='wide', page_title='mera code')

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

def load_investor_details(investor):
    st.title(investor)
    # load the recent 5 investments of the investor 
    last5_df = df[df['investors'].str.contains(investor)].head()[['date', 
                            'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader("Most Recent Investments")
    st.dataframe(last5_df)
    
    col1, col2 = st.columns(2)
    
    with col1:
    # biggest investments 
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum(
            ).sort_values(ascending=False).head()
        st.subheader("Biggest Investments")
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)
    with col2:
        round_series = df[df['investors'].str.contains(investor)].groupby(
        'round')['amount'].sum()
        st.subheader("Round funding")
        fig1, ax1 = plt.subplots()
        ax1.pie(round_series, labels=round_series.index, autopct='%.2f')
        st.pyplot(fig1) 
    
    col3, col4 = st.columns(2)
    with col3:
    #   
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')[
                'amount'].sum()
        st.subheader("Sectors invested")
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series, labels=vertical_series.index, autopct='%.2f')
        st.pyplot(fig1)
    
    with col4:
        # Which city 
        city_series = df[df['investors'].str.contains(investor)].groupby('city')[
                'amount'].sum()
        st.subheader("City invester")
        fig1, ax1 = plt.subplots()
        ax1.pie(city_series, labels=city_series.index, autopct='%.2f')
        st.pyplot(fig1)
        
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains('IDG Ventures')].groupby(
        'year')['amount'].sum()
    st.subheader("Yoy Investmen")
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index, year_series.values)
    st.pyplot(fig2)
        
def load_overall_analysis():
    st.title('over all analysis')
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
    # Total invested amount 
        total = round(df['amount'].sum(), 4)
        st.metric('Total', str(total) + 'Cr')
    
    with col2:
        # Maximum amount used in a startup 
        max_amount = df.groupby('startup')['amount'].max().sort_values(
            ascending=False).head(1).values[0]
        st.metric('Maximum Finding', str(max_amount) + 'Cr')
    
    with col3:
        # Average ticket size
        avg_funding = round(df.groupby('startup')['amount'].sum().mean(), 3)
        st.metric("Avg", str(avg_funding) + 'Sr')
        
    with col4:
        # Total funded startup 
        num_startup = df['startup'].nunique()
        st.metric("Funded Startup", num_startup)
        
    
    st.header('Month on Month graph')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
    temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)
    # temp_df[['amount', 'x_axis']]
    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig3)
    
st.sidebar.title("Startup Funding Analysis")

option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])

if option == 'Overall Analysis':
    # st.title('Overall Analysis')
    # st.subheader("Bad me akke data cleaning kar dena ")
    btn0 = st.sidebar.button('Show overall Analysis')
    if btn0:
        load_overall_analysis()
      
elif option == 'Startup':
    st.sidebar.selectbox('Select Starup', sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('Startup Analysis')
else:
    selected_investor = st.sidebar.selectbox('Select Starup', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)
        
    # st.title('Startup Investor')
