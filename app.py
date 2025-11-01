#Libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import scipy
import plotly.figure_factory as ff

from func.preprocessor import preprocess
from func.helper import yearwise_medal_tally,medal_tally , country_year_list , fetch_medal_tally , data_over_time , most_successfull , country_event , most_successfull_countrywise , weight_v_height ,men_vs_women

# Load the Data
df = pd.read_csv('data/athlete_events.csv')
region_df = pd.read_csv('data/noc_regions.csv')

df = preprocess(df,region_df)

st.set_page_config(
    page_title="Olympics Data Analysis Dashboard",
    page_icon="🏅",
    layout="wide",  # 👈 This makes the screen always open in wide mode
)

st.sidebar.title("Olympics Data Analysis")
user_menu = st.sidebar.radio(
    "Select an Option",
    (
        "Home",
        "Medals Tally",
        "Overall Analysis",
        "Country-wise-Analysis",
        "Athlete-wise-Analysis"
    )
)

# --- Landing Page / Home ---
if user_menu == 'Home':
    st.title("Olympics Data Analysis Dashboard")
    st.markdown("---")

    # 🧭 Overview Section
    st.subheader("📘 Project Overview")
    st.write("""
    This interactive dashboard provides an in-depth analysis of the **Olympic Games** dataset,
    offering insights into medals, athletes, countries, and historical trends.

    The goal of this project is to help users **visualize Olympic data dynamically**, 
    explore **medal tallies**, **athlete performance**, and track **gender participation** 
    across different editions of the Olympics.
    """)

    # 🧩 Dataset Information
    st.subheader("📊 Dataset Details")
    st.write("""
    The dataset used for this project is derived from the **Olympics dataset on Kaggle**, which contains:
    - 🧍‍♂️ **Athlete Information** (Name, Sex, Age, Height, Weight)
    - 🏆 **Medal Details** (Gold, Silver, Bronze)
    - 🌍 **Country / Region** participation
    - ⚽ **Sport & Event information**
    - 📅 **Year & Season (Summer/Winter Olympics)**

    This dataset spans over **120 years** of Olympic history, helping visualize long-term performance patterns.
    """)

    # 📈 Features Summary
    st.subheader("🚀 Features of This Dashboard")
    st.markdown("""
    - **Medal Tally:** View medals by country, year, and overall performance.
    - **Athlete-wise Analysis:** Explore age, height, and weight distribution of athletes.
    - **Country-wise Analysis:** Track country performance and dominance over the years.
    - **Event Trends:** See how participation and sports popularity have evolved.
    - **Gender Analysis:** Compare male vs female participation growth through time.
    """)

    # 🧠 Technology Stack
    st.subheader("💻 Technology Stack")
    st.markdown("""
    - **Frontend:** Streamlit  
    - **Data Handling:** Pandas, NumPy  
    - **Visualization:** Plotly, Seaborn, Matplotlib  
    - **Language:** Python  
    """)

    st.markdown("---")
    st.info("Use the sidebar to navigate between sections like Medal Tally, Athlete-wise Analysis, and more.")
    st.success("Data Source: [Kaggle - 120 Years of Olympic History Dataset](https://www.kaggle.com/datasets/mysarahmadbhat/120-years-of-olympic-history-athletes-and-results)")


elif user_menu == 'Medals Tally':

    st.sidebar.header('Medal Tally')
    years,country = country_year_list(df)

    selected_year = st.sidebar.selectbox('Select Year' , years)
    selected_country = st.sidebar.selectbox('Select Country' , country)

    medal_tally = medal_tally(df)

    medal_tally = fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.header('Overall Metal Tally')

    if selected_year != 'Overall' and selected_country == 'Overall':
        st.header('Medal Tally in ' + str(selected_year) + ' Olympics')

    if selected_year == 'Overall' and selected_country != 'Overall':
        st.header(selected_country + ' Overall Performance')

    if selected_year != 'Overall' and selected_country != 'Overall':
        st.header(selected_country + ' Performance ' + str(selected_year) + ' Olympics.')
        
    st.dataframe(medal_tally)

elif user_menu == 'Overall Analysis':

    st.title("🏅 Olympics Overview Dashboard")
    st.markdown("---")
    # ======= Overview Metrics =======
    editions = df['Year'].nunique()
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    # ---- Create Tabs ----
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Trends Over Time", "🎯 Events by Sport", "🏅 Top Athletes"])

    # =============================================================
    # 📊 TAB 1 — Overview Metrics
    # =============================================================
    with tab1:
        st.subheader("📊 General Overview")
        st.caption("Key statistics from the Summer Olympics dataset")

        col1, col2, col3 = st.columns(3)
        col1.metric("Editions", editions)
        col2.metric("Host Cities", cities)
        col3.metric("Sports", sports)

        col4, col5, col6 = st.columns(3)
        col4.metric("Events", events)
        col5.metric("Athletes", athletes)
        col6.metric("Nations", nations)

    # =============================================================
    # 📈 TAB 2 — Trends Over Time
    # =============================================================
    with tab2:
        st.subheader("📈 Trends Over the Years")
        st.caption("Explore how participation and events evolved across Olympic editions.")

        nations_over_time = data_over_time(df, 'region')
        events_over_time = data_over_time(df, 'Event')
        athletes_over_time = data_over_time(df, 'Name')

        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.line(nations_over_time, x="Editions", y="region", title="Participating Nations Over the Years")
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig2 = px.line(events_over_time, x="Editions", y="Event", title="Events Over the Years")
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")
        fig3 = px.line(athletes_over_time, x="Editions", y="Name", title="Athletes Over the Years")
        st.plotly_chart(fig3, use_container_width=True)

    # =============================================================
    # 🎯 TAB 3 — Events by Sport
    # =============================================================
    with tab3:
        st.subheader("🎯 Events per Sport (Interactive)")
        st.caption("Compare the number of unique events across different sports over time.")

        x = df.drop_duplicates(['Year', 'Sport', 'Event'])
        events_per_sport = x.groupby(['Year', 'Sport'])['Event'].count().reset_index()

        fig4 = px.line(
            events_per_sport,
            x='Year',
            y='Event',
            color='Sport',
            title='Number of Events Over Time by Sport'
        )
        st.plotly_chart(fig4, use_container_width=True)

    # =============================================================
    # 🏅 TAB 4 — Most Successful Athletes
    # =============================================================
    with tab4:
        st.subheader("🏅 Most Successful Athletes")
        st.caption("View top-performing athletes across all sports or a specific discipline.")

        sport_list = df['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0, 'Overall')

        selected_sport = st.selectbox("Select a Sport", sport_list, key="athlete_sport")
        x = most_successfull(df, selected_sport)

        st.dataframe(x, use_container_width=True)


elif user_menu == 'Country-wise-Analysis':
    st.title("🌍 Country-Wise Olympic Analysis")
    st.markdown("---")

    # Sidebar: Country Selection
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox("🏳️ Select a Country", country_list)

    # Tabs for better organization
    tab1, tab2, tab3 = st.tabs(["🏅 Medal Trends", "⚽ Sports Performance", "👑 Top Athletes"])

    # ------------------- TAB 1: Medal Trends -------------------
    with tab1:
        st.subheader(f"{selected_country} — Medal Tally Over the Years")
        country_df = yearwise_medal_tally(df, selected_country)

        fig = px.line(
            country_df,
            x='Year',
            y='Medal',
            markers=True,
            color_discrete_sequence=['#00BFFF'],
            title=f"{selected_country} Medal Trend Over Time"
        )
        fig.update_layout(
            template='plotly_dark',
            xaxis_title="Year",
            yaxis_title="Number of Medals",
            title_x=0.3
        )
        st.plotly_chart(fig, use_container_width=True)

    # ------------------- TAB 2: Sports Performance -------------------
    with tab2:
        st.subheader(f"🏆 {selected_country} Excels in These Sports")
        pt = country_event(df, selected_country)

        fig, ax = plt.subplots(figsize=(14, 8))
        sns.heatmap(pt, annot=True, linewidths=0.5, fmt='g', ax=ax)
        ax.set_title(f"{selected_country} — Performance by Sport", fontsize=14, fontweight='bold')
        st.pyplot(fig)

    # ------------------- TAB 3: Top Athletes -------------------
    with tab3:
        st.subheader(f"👑 Most Successful Athletes from {selected_country}")
        top10_df = most_successfull_countrywise(df, selected_country)
        st.dataframe(top10_df)


elif user_menu == 'Athlete-wise-Analysis':

    st.title("Athlete-wise-Analysis")
    st.markdown("---")

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    # --- Create Tabs ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏅 Age Distribution",
        "⚽ Age vs Sport (Gold Medalists)",
        "📏 Height vs Weight",
        "👨‍🦰 Men vs 👩‍🦱 Women Participation"
    ])

    # -----------------------------------
    # 🏅 TAB 1: Age Distribution
    # -----------------------------------
    with tab1:
        x1 = athlete_df['Age'].dropna()
        x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
        x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
        x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

        fig = ff.create_distplot(
            [x1, x2, x3, x4],
            ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
            show_hist=False, show_rug=False
        )
        fig.update_layout(autosize=False, width=1000, height=600)
        st.subheader("Distribution of Age Among Athletes")
        st.plotly_chart(fig, use_container_width=True)

    # -----------------------------------
    # ⚽ TAB 2: Age Distribution per Sport (Gold Medalists)
    # -----------------------------------
    with tab2:
        x = []
        name = []
        famous_sport = [
            'Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics', 'Swimming',
            'Badminton', 'Sailing', 'Gymnastics', 'Art Competitions', 'Handball',
            'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey', 'Rowing', 'Fencing',
            'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
            'Tennis', 'Golf', 'Softball', 'Archery', 'Volleyball',
            'Synchronized Swimming', 'Table Tennis', 'Baseball', 'Rhythmic Gymnastics',
            'Rugby Sevens', 'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey'
        ]

        for sport in famous_sport:
            temp_df = athlete_df[athlete_df['Sport'] == sport]
            x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
            name.append(sport)

        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=1000, height=600)
        st.subheader("Age Distribution of Gold Medalists by Sport")
        st.plotly_chart(fig, use_container_width=True)

    # -----------------------------------
    # 📏 TAB 3: Height vs Weight Scatter Plot
    # -----------------------------------
    with tab3:
        sport_list = df['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0, 'Overall')

        st.subheader("Height vs Weight Comparison")
        selected_sport = st.selectbox("Select a Sport", sport_list, key='sport_select')

        temp_df = weight_v_height(df, selected_sport)
        fig, ax = plt.subplots()
        sns.scatterplot(
            x='Weight',
            y='Height',
            data=temp_df,
            hue='Medal',
            style='Sex',
            ax=ax,
            s=70,
            alpha=0.7
        )
        ax.set_title(f"Height vs Weight ({selected_sport})", fontsize=14)
        st.pyplot(fig)

    # -----------------------------------
    # 👨‍🦰 TAB 4: Men vs Women Participation
    # -----------------------------------
    with tab4:
        st.subheader("Men vs Women Participation Over the Years")
        final = men_vs_women(df)
        fig = px.line(final, x='Year', y=['Male', 'Female'],
                      title='Men vs Women Participation Trend',
                      markers=True)
        st.plotly_chart(fig, use_container_width=True)


    


