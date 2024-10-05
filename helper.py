import streamlit as st
import numpy as np
import pandas as pd


def fetch_medal(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = (medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].
                   sort_values('Gold',
                               ascending=False).reset_index())
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype(int)
    medal_tally['Silver'] = medal_tally['Silver'].astype(int)
    medal_tally['Bronze'] = medal_tally['Bronze'].astype(int)
    medal_tally['Total'] = medal_tally['Total'].astype(int)
    return medal_tally


def country_year_analysis(df):
    year = df['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'Overall')
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return year, country


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        st.title('Overall Medal Tally')
        medal_df = medal_df
    if year == 'Overall' and country != 'Overall':
        st.title('Overall Medal Tally for country ' + str(country))
        flag = 1
        medal_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        st.title('Overall Medal Tally for year ' + str(year))
        medal_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        st.title('Medal Tally for ' + str(country) + ' in year ' + str(year))
        medal_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        medal_df = medal_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        medal_df = medal_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                              ascending=False).reset_index()

    medal_df['Total'] = medal_df['Gold'] + medal_df['Silver'] + medal_df['Bronze']
    return medal_df


def data_over_year(df, col):
    nations_over_time_df = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    nations_over_time_df.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
    return nations_over_time_df


def most_successful_athlete(df, sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    temp_df = temp_df['Name'].value_counts().reset_index().head(15)
    temp_df.rename(columns={'index': 'Name', 'Name': 'no of medals'}, inplace=True)
    final_df = temp_df.merge(df, left_on='Name', right_on='Name', how='left').drop_duplicates(subset=['Name'])
    final_df = final_df[['Name', 'Sport', 'no of medals', 'region']].reset_index()
    final_df = final_df.drop('index', axis=1)
    return final_df


def year_wise_medal_of_country(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    final_df = temp_df.groupby('Year').count()['Medal'].reset_index()
    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    new_df = temp_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return new_df


def most_successful_athlete_country_wise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    temp_df = temp_df['Name'].value_counts().reset_index().head(10)
    temp_df.rename(columns={'index': 'Name', 'Name': 'no of medals'}, inplace=True)
    final_df = temp_df.merge(df, left_on='Name', right_on='Name', how='left').drop_duplicates(subset=['Name'])
    final_df = final_df[['Name', 'Sport', 'no of medals']].reset_index()
    final_df = final_df.drop('index', axis=1)
    return final_df


def men_vs_women_analysis(athlete_df):
    male_df = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    female_df = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    male_female_df = male_df.merge(female_df, how='left', on='Year')
    male_female_df.fillna(0, inplace=True)
    male_female_df.rename(columns={'Name_x': 'male', 'Name_y': 'female'}, inplace=True)
    return male_female_df
