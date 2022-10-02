import streamlit as st
import pandas as pd
import numpy as np
import matplotlib as plt
import helper
import plotly.express as px
import json

df = pd.read_csv('India Census 2011.csv')

df_new = df.copy()


st.sidebar.title('Census Data Analysis')
st.sidebar.image('https://thumbs.dreamstime.com/b/census-word-cloud-concept-grey-background-90879126.jpg')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('State', 'District', 'Overall Analysis')
)

# =======================================STATE ANALYSIS===================================================

if user_menu == 'State':
    state = helper.state_list(df)

    Selected_State = st.sidebar.selectbox('STATE NAME', state)
    state_pop = helper.fetch_state_data(Selected_State).style.format(thousands=",")

    if Selected_State == 'Overall':

        st.title('Indian Population Density')
        st.caption('Note: Due to map plot it may take a while for page loading')
        map_fig = helper.india_map(df_new)
        st.plotly_chart(map_fig)


        st.header('State-Wise Population of different Religions')
        religion_pop = helper.state_rel_pop(Selected_State).style.format(thousands=",")
        st.dataframe(religion_pop)

        st.header('Educated Count of different States')
        educated_pop = helper.Edu_of_pop(Selected_State).style.format(thousands=",")
        st.dataframe(educated_pop)

        st.header('State-Wise Age Group Population')
        age_grp_pop = helper.Age_pop(Selected_State)
        # for i in age_grp_pop:
        #     st.plotly_chart(age_grp_pop[i])


    if Selected_State != 'Overall':
        st.title('Total Population of ' + Selected_State)
        st.dataframe(state_pop)

        st.header('Population of different Religions')
        religion_pop = helper.state_rel_pop(Selected_State)
        st.dataframe(religion_pop)

        st.header('Educated Count of this State')
        educated_pop = helper.Edu_of_pop(Selected_State)
        st.dataframe(educated_pop)

        st.header('Population of different Age Groups')
        age_grp_pop = helper.Age_pop(Selected_State)
        st.dataframe(age_grp_pop)

# =======================================DISTRICT ANALYSIS===================================================

if user_menu == 'District':
    district = helper.district_list(df)

    Selected_district = st.sidebar.selectbox('DISTRICT NAME', district)
    dist_pop = helper.fetch_district_data(Selected_district).style.format(thousands=",")

    if Selected_district == 'Overall':
        st.title('Overall District-Wise Population')
        st.dataframe(dist_pop)

        st.header('District-Wise Literacy Percentage')
        literacy_dist_per = helper.Literacy_dist(Selected_district)
        st.dataframe(literacy_dist_per)

    if Selected_district != 'Overall':
        st.title('Total Population of ' + Selected_district)
        st.dataframe(dist_pop)

        st.header('Literacy Percentage of ' + Selected_district)
        literacy_dist_per = helper.Literacy_dist(Selected_district)
        st.dataframe(literacy_dist_per)

        st.header('Worker Count of ' + Selected_district)
        worker_count = helper.Worker_plot(Selected_district).style.format(thousands=",")
        st.dataframe(worker_count)
        

# =======================================OVERALL ANALYSIS======================================================         

if user_menu == 'Overall Analysis':

    States_No = df['State_name'].unique().shape[0]
    District_No = df['District_name'].unique().shape[0]
    Male_pop = df['Male'].sum()
    Female_pop = df['Female'].sum()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('#### Total States')
        # st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)
        st.subheader(States_No)

    with col2:
        st.markdown('#### Total Districts')
        st.subheader(District_No)    

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("")
    with col2:
        st.subheader("")
         

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('#### Total Male Population')
        st.subheader(format(Male_pop,','))

    with col2:
        st.markdown('#### Total Female Population')
        st.subheader(format(Female_pop,','))   

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("")
        st.subheader("")
    with col2:
        st.subheader("")
        st.subheader("")

    count =df['State_name'].value_counts()
    count = pd.DataFrame(count).reset_index()
    count.rename(columns={'index':'State_name', 'State_name': 'Count'}, inplace=True)

    x1 = count['State_name'].unique().tolist()
    y1 = count['Count'].tolist()

    st.markdown('#### -- Districts per State :')
    fig = px.bar(data_frame=count, x=x1, y=y1)
    fig.update_layout(
        # title="Districts per State",
        xaxis_title="States",
        yaxis_title="Count",
    )
    st.plotly_chart(fig,use_container_width=True)


    st.markdown('#### -- Workers per State :')
    worker_statewise_plot = helper.Worker_State_plot(True)

