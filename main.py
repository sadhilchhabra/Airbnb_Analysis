import pandas as pd
import pymongo
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu

# -------------------------------This is the configuration page for our Streamlit Application---------------------------
st.set_page_config(
    page_title="AirBnb Analysis",
    page_icon="🏨",
    layout="wide"
)

# -------------------------------This is the sidebar in a Streamlit application, helps in navigation--------------------
with st.sidebar:
    selected = option_menu("Main Menu", ["About Project", "Basic Overview", "Data Visualization", "Exploration"],
                           icons=["house", "gear", "tools", "bar-chart"],
                           styles={"nav-link": {"font": "sans serif", "font-size": "20px", "text-align": "centre"},
                                   "nav-link-selected": {"font": "sans serif", "background-color": "#e5b252"},
                                   "icon": {"font-size": "20px"}
                                   }
                           )

# -------------------------------Connecting to MongoDB Atlas Database and accessing the collections---------------------
client = pymongo.MongoClient("mongodb+srv://sadhil:gNft43QEaHs0aavO@airbnb.nicvmej.mongodb.net/",
                             serverSelectionTimeoutMS=10000)
db = client['sample_airbnb']
mycol = db['listingsAndReviews']

# ------------Error Handling for MongoDB Atlas Connection Timeout Error------------
# try:
#     # Try to access a MongoDB command to check if the connection is successful
#     client.server_info()
#     st.success("You are successfully connected to MongoDB Atlas!")
# except Exception as e:
#     st.error(f"An error occurred: {e}")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# -------------------------Reading the Airbnb_data.csv file that we created after Data Cleaning-------------------------
df = pd.read_csv('Airbnb_data.csv')

# -----------------------------------------------About Project Section--------------------------------------------------
if selected == "About Project":
    st.markdown("# :orange[Airbnb Analysis]")
    st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
    st.markdown("### :orange[Technologies :] Python, Pandas, Plotly, Streamlit, MongoDB, Python scripting, "
                "Data Preprocessing, Visualization, EDA")
    st.markdown("### :orange[Overview :] To conduct an analysis of Airbnb data using MongoDB Atlas, the process "
                "involves cleaning and preparing the data, creating interactive visualizations, and generating "
                "dynamic plots. The goal is to extract insights regarding price fluctuations, availability trends, "
                "and location-based patterns within the dataset.")
    st.markdown("### :orange[Domain :] Travel Industry, Property Management and Tourism")

# -----------------------------------------------Basic Overview Section-------------------------------------------------
if selected == "Basic Overview":
    st.markdown("# :orange[Basic Overview of Airbnb Data]")
    # -----Creating Filter option for user inputs-----
    country = st.sidebar.multiselect('Select a Country :',
                                     sorted(df.Country.unique()),
                                     sorted(df.Country.unique())
                                     )
    property1 = st.sidebar.multiselect('Select Property Type :',
                                       sorted(df.Property_type.unique()),
                                       sorted(df.Property_type.unique())
                                       )
    room = st.sidebar.multiselect('Select Room Type :',
                                  sorted(df.Room_type.unique()),
                                  sorted(df.Room_type.unique())
                                  )
    price = st.slider('Select Price :', df.Price.min(), df.Price.max(),
                      (df.Price.min(), df.Price.max())
                      )

    # -----Taking the user inputs and merging then with MongoDB Query for Data Retrieval-----
    query = f'Country in {country} & Room_type in {room} & Property_type in {property1} & Price >= {price[0]} & Price <= {price[1]}'

    # -----Top 10 Property Types-----
    df1 = df.query(query)
    counts_df1 = df1.groupby(["Property_type"]).size().reset_index(name="count").sort_values(by='count',
                                                                                             ascending=False).head(10)
    fig = px.bar(counts_df1,
                 title='Top 10 Property Types',
                 x='count',
                 y='Property_type',
                 color='Property_type'
                 )
    fig.update_yaxes(title='Property Type')
    fig.update_xaxes(title='Count')
    st.plotly_chart(fig, use_container_width=True)

    # -----Top 10 Hosts with Highest number of Listings-----
    df2 = df.query(query)
    counts_df2 = df2.groupby(["Host_name"]).size().reset_index(name="count").sort_values(by='count',
                                                                                         ascending=False).head(10)
    fig = px.bar(counts_df2,
                 title='Top 10 Hosts with Highest number of Listings',
                 x='count',
                 y='Host_name',
                 color='Host_name'
                 )
    fig.update_yaxes(title='Host Name')
    fig.update_xaxes(title='Count')
    st.plotly_chart(fig, use_container_width=True)

    # -----Data of each Room Types-----
    df3 = df.query(query)
    counts_df3 = df3.groupby(["Room_type"]).size().reset_index(name="count")
    fig = px.pie(counts_df3,
                 title='Data of each Room Types',
                 names='Room_type',
                 values='count'
                 )
    fig.update_traces(textposition='outside', textinfo='value+label')
    st.plotly_chart(fig, use_container_width=True)

    # -----Total counts/listings based on Countries-----
    df4 = df.query(query)
    country_df = df4.groupby(['Country'], as_index=False)['Name'].count().rename(columns={'Name': 'count'})
    fig = px.choropleth(country_df,
                        title='Total Listings in each Country :',
                        locations='Country',
                        locationmode='country names',
                        color='count',
                        )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------Data Analysis and Visualization Section----------------------------------------
if selected == "Data Visualization":
    st.markdown("# :orange[Data Analysis and Visualization]")
    st.sidebar.header("Visualization Options:")

    # ----------Analysis of Numerical Data in the DataFrame----------
    st.sidebar.subheader("Analysis of Numerical Data in the DataFrame")
    if st.sidebar.checkbox("Display Statistics"):
        st.markdown('<h3 style="color:#5DBB63">Various Stats of the Numerical Data Columns of the DataFrame</h3>',
                    unsafe_allow_html=True)
        st.write(df.describe())

    # ----------Display Histogram of Selected Column----------
    st.sidebar.subheader("Target Analysis")
    if st.sidebar.checkbox("Display Histogram of Selected Column"):
        all_columns = st.sidebar.multiselect("Select a column :", df.columns)
        for column0 in all_columns:
            st.markdown(f'<h3 style="color:#5DBB63">Histogram of {column0}</h3>',
                        unsafe_allow_html=True)
            fig = px.histogram(df, x=column0, color_discrete_sequence=['#E1E6E1'])
            st.plotly_chart(fig)

    # ----------Display Histogram for Numerical Columns Only----------
    st.sidebar.subheader("Distribution of Numerical Columns")
    if st.sidebar.checkbox("Display Histogram for Numerical Columns Only"):
        numerical_columns = df.select_dtypes(exclude='object').columns
        selected_numerical_columns = st.sidebar.multiselect("Select numerical columns for the histogram plot :",
                                                            numerical_columns)
        for column1 in selected_numerical_columns:
            st.markdown(f'<h3 style="color:#5DBB63">Histogram for {column1}</h3>',
                        unsafe_allow_html=True)
            fig = px.histogram(df, x=column1, color_discrete_sequence=['#E1E6E1'])
            st.plotly_chart(fig)

    # ----------Display Histogram for Categorical Columns----------
    st.sidebar.subheader("Count Plots of Categorical Columns")
    if st.sidebar.checkbox("Display Histogram for Categorical Columns"):
        categorical_columns = df.select_dtypes(include='object').columns
        selected_categorical_columns = st.sidebar.multiselect("Select categorical columns for count plots:",
                                                              categorical_columns)
        for column2 in selected_categorical_columns:
            st.markdown(f'<h3 style="color:#5DBB63">Histogram for {column2}</h3>',
                        unsafe_allow_html=True)
            fig = px.histogram(df, x=column2, color_discrete_sequence=['#E1E6E1'])
            st.plotly_chart(fig)

    # ----------Display Box Plots----------
    st.sidebar.subheader("Box Plots")
    if st.sidebar.checkbox("Display Box Plots"):
        numerical_columns = df.select_dtypes(exclude='object').columns
        selected_numerical_columns = st.sidebar.multiselect("Select numerical columns for box plots:",
                                                            numerical_columns)
        for column3 in selected_numerical_columns:
            st.markdown(f'<h3 style="color:#5DBB63">Box Plot of {column3}</h3>',
                        unsafe_allow_html=True)
            fig = px.box(df, y=column3)
            st.plotly_chart(fig)

    # ----------Display Outlier Counts----------
    st.sidebar.subheader("Outlier Analysis")
    if st.sidebar.checkbox("Display Outlier Counts"):
        st.markdown(f'<h3 style="color:#5DBB63">Outlier Analysis</h3>',
                    unsafe_allow_html=True)
        outlier_df = df.select_dtypes(exclude='object').apply(lambda x: sum((x - x.mean()) > 2 * x.std())).reset_index(
            name="outliers")
        st.write(outlier_df)

# -----------------------------------------------Exploration Section----------------------------------------------------
if selected == "Exploration":
    st.markdown("# :orange[Data Exploration]")

    # -----Creating Filter option for user inputs-----
    country = st.sidebar.multiselect('Select a Country :',
                                     sorted(df.Country.unique()),
                                     sorted(df.Country.unique())
                                     )
    property1 = st.sidebar.multiselect('Select Property Type :',
                                       sorted(df.Property_type.unique()),
                                       sorted(df.Property_type.unique())
                                       )
    room = st.sidebar.multiselect('Select Room Type :',
                                  sorted(df.Room_type.unique()),
                                  sorted(df.Room_type.unique())
                                  )
    price = st.slider('Select Price :', df.Price.min(), df.Price.max(),
                      (df.Price.min(), df.Price.max())
                      )

    # -----Taking the user inputs and merging then with MongoDB Query for Data Retrieval-----
    query = f'Country in {country} & Room_type in {room} & Property_type in {property1} & Price >= {price[0]} & Price <= {price[1]}'

    # -----Different Room Types based on their Average Booking Price-----
    df5 = df.query(query)
    price_df1 = df5.groupby('Room_type', as_index=False)['Price'].mean().sort_values(by='Price')
    fig = px.bar(price_df1,
                 x='Room_type',
                 y='Price',
                 color='Price',
                 title='Different Room Types based on their Average Booking Price',
                 color_continuous_scale='Viridis'
                 )
    st.plotly_chart(fig, use_container_width=True)

    # -----Different Countries based on their Average Booking Price-----
    df6 = df.query(query)
    price_df2 = df6.groupby('Country', as_index=False)['Price'].mean().sort_values(by='Price')
    fig = px.bar(price_df2,
                 x='Country',
                 y='Price',
                 color='Price',
                 title='Different Countries based on their Average Booking Price',
                 color_continuous_scale='Viridis'
                 )
    st.plotly_chart(fig, use_container_width=True)

    # -----Availability by Room Type-----
    df7 = df.query(query)
    fig = px.box(df7,
                 x='Room_type',
                 y='Availability_365',
                 color='Room_type',
                 title='Availability by Room Type :'
                 )
    st.plotly_chart(fig, use_container_width=True)

    # -----Different Countries based on their Average Booking Price ==> SCATTERED PLOT-----
    df8 = df.query(query)
    country_df1 = df8.groupby('Country', as_index=False)['Price'].mean()
    fig = px.scatter_geo(data_frame=country_df1,
                         locations='Country',
                         color='Price',
                         size='Price',
                         locationmode='country names',
                         title='Different Countries based on their Average Booking Price ==> SCATTERED PLOT',
                         )
    st.plotly_chart(fig, use_container_width=True)

    # -----Different Countries based on their Average Availability ==> SCATTERED PLOT-----
    df9 = df.query(query)
    country_df2 = df9.groupby('Country', as_index=False)['Availability_365'].mean()
    country_df2.Availability_365 = country_df2.Availability_365.astype(int)
    fig = px.scatter_geo(data_frame=country_df2,
                         locations='Country',
                         color='Availability_365',
                         size='Availability_365',
                         locationmode='country names',
                         title='Different Countries based on their Average Availability ==> SCATTERED PLOT'
                         )
    st.plotly_chart(fig, use_container_width=True)