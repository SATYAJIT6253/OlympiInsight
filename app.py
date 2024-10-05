import streamlit as st
import pandas as pd
import prepocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = prepocessor.preprocess(df, region_df)
st.sidebar.title('Olympic Data Analysis')
user_menu = st.sidebar.radio(
    "Choose a shipping method",
    ("Medal Tally", "overall analysis", "country-wise Analysis", "Athlete wise Analysis")
)
# st.dataframe(df)

if user_menu == 'Medal Tally':
    # medal_tally = helper.fetch_medal(df)
    st.sidebar.subheader('Medal Tally')
    years, country = helper.country_year_analysis(df)
    selected_year = st.sidebar.selectbox("select year", years)
    selected_country = st.sidebar.selectbox("select country", country)
    medal_df = helper.fetch_medal_tally(df, selected_year, selected_country)
    st.table(medal_df)

if user_menu == 'overall analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.subheader("Editions  ")
        st.subheader(editions)
    with col2:
        st.subheader("Hosts  ")
        st.subheader(cities)
    with col3:
        st.subheader("Sports")
        st.subheader(sports)
    with col4:
        st.subheader("Events  ")
        st.subheader(events)
    with col5:
        st.subheader("Nations  ")
        st.subheader(nations)
    with col6:
        st.subheader("Athletes  ")
        st.subheader(athletes)

    nations_over_time_df = helper.data_over_year(df, 'region')
    fig = px.line(nations_over_time_df, x="Edition", y="region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time_df = helper.data_over_year(df, 'Event')
    fig = px.line(events_over_time_df, x="Edition", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athletes_over_time_df = helper.data_over_year(df, 'Name')
    fig = px.line(athletes_over_time_df, x="Edition", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('select sports', sport_list)
    successful_athlete_df = helper.most_successful_athlete(df, selected_sport)
    st.table(successful_athlete_df)

if user_menu == 'country-wise Analysis':
    st.sidebar.title('Country wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('select country', country_list)
    country_wise_df = helper.year_wise_medal_of_country(df, selected_country)
    fig = px.line(country_wise_df, x='Year', y='Medal')
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title("medal win by" + selected_country)
    new_df = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax = sns.heatmap(new_df, annot=True)
    st.pyplot(fig)

    st.title("top 10 successful athlete of country" + selected_country)
    successful_ath_country_wise_df = helper.most_successful_athlete_country_wise(df, selected_country)
    st.table(successful_ath_country_wise_df)

if user_menu == 'Athlete wise Analysis':
    st.title('Distribution of Age')
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    group_labels = ['Overall Distribution', 'Gold medalist', 'Silver medalist', 'Bronze medalist']
    fig = ff.create_distplot([x1, x2, x3, x4], group_labels, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=900, height=500)
    st.plotly_chart(fig)

    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    X = []
    group_labels = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        X.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        group_labels.append(sport)
    fig1 = ff.create_distplot(X, group_labels, show_hist=False, show_rug=False)
    fig1.update_layout(autosize=False, width=900, height=750)
    st.plotly_chart(fig1)

    st.title("Distribution of Age wrt Sports(Silver Medalist)")
    X = []
    group_labels = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        X.append(temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna())
        group_labels.append(sport)
    fig1 = ff.create_distplot(X, group_labels, show_hist=False, show_rug=False)
    fig1.update_layout(autosize=False, width=900, height=750)
    st.plotly_chart(fig1)

    st.title("Men Vs Women Participation Over the Years")
    men_women_df = helper.men_vs_women_analysis(athlete_df)
    fig = px.line(men_women_df, x='Year', y=['male', 'female'], width=850, height=600)
    st.plotly_chart(fig)
