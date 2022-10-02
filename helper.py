import numpy as np
import pandas as pd
import matplotlib as plt
import json
import plotly.express as px
import streamlit as st

df = pd.read_csv('India Census 2011.csv')

# ==========================================FOR STATE ANALYSIS=================================================

St_name = df.groupby('State_name').Population.sum().sort_values(ascending = False)
St_name = pd.DataFrame(St_name, index=None).reset_index()
St_name.set_index('State_name').style.format(thousands=",")

def Age_pop(state):
    Overall_AgeGrp_pop = df.groupby('State_name')['Age_Group_0_29','Age_Group_30_49','Age_Group_50'].sum()
    Overall_AgeGrp_pop = pd.DataFrame(Overall_AgeGrp_pop).reset_index()
    Overall_AgeGrp_pop.set_index('State_name').style.format(thousands=",")

    if state == "Overall":
        fig1 = px.bar(Overall_AgeGrp_pop, x="State_name", y="Age_Group_0_29",text_auto='.2s',title="Total Population of Age Group 0-29(Yrs)")
        fig2 = px.bar(Overall_AgeGrp_pop, x="State_name", y="Age_Group_30_49",text_auto='.2s',title="Total Population of Age Group 30-49(Yrs)")
        fig3 = px.bar(Overall_AgeGrp_pop, x="State_name", y="Age_Group_50",text_auto='.2s',title="Total Population of Age Group 50(Yrs)")
       
        return st.plotly_chart(fig1),st.plotly_chart(fig2),st.plotly_chart(fig3)
       
        
    elif state != "Overall":
        x = Overall_AgeGrp_pop.loc[Overall_AgeGrp_pop['State_name'] == state].style.format(thousands=",") 
        return x


def india_map(df_new):
    india_states = json.load(open("states_india.geojson", "r"))
    
    state_id_map = {}
    for feature in india_states["features"]:
        feature["id"] = feature["properties"]["state_code"]
        state_id_map[feature["properties"]["st_nm"]] = feature["id"]

    St_name["id_of_States"] = St_name["State_name"].apply(lambda x: state_id_map[x])

    St_name["Population_Scale"] = np.log10(St_name["Population"])

    fig = px.choropleth_mapbox(
        St_name,
        locations="id_of_States",
        geojson=india_states,
        color="Population",
        hover_name="State_name",
        hover_data=["Population"],
        mapbox_style="carto-positron",
        center={"lat": 24, "lon": 78},
        zoom=3,
        opacity=0.5,
    )

    return fig


def fetch_state_data(state):
    if state == 'Overall':
        temp_df = St_name
    else:
        temp_df = St_name[St_name['State_name'] == state]   
        
    return temp_df

def state_rel_pop(state):
    religion_pop = df.groupby('State_name')['Hindus','Muslims','Christians','Buddhists','Sikhs','Jains'].sum().sort_values(by = 'Hindus', ascending = False)
    religion_pop = pd.DataFrame(religion_pop).reset_index()
    # religion_pop.set_index('State_name').style.format(thousands=",")
    religion_pop.set_index('State_name')

    if state == "Overall":
        x = religion_pop
    if state != "Overall":
        x = religion_pop.loc[religion_pop['State_name'] == state].style.format(thousands=",") 
    return x

def Edu_of_pop(state):
    Edu_of_pop = df.groupby('State_name')['Secondary_Education','Higher_Education','Graduate_Education'].sum()
    Edu_of_pop = pd.DataFrame(Edu_of_pop).reset_index() 
    Edu_of_pop.set_index('State_name')

    if state == "Overall":
        x = Edu_of_pop
    if state != "Overall":
        x = Edu_of_pop.loc[Edu_of_pop['State_name'] == state].style.format(thousands=",") 
    return x    


# To Fetch the State List from the SideBar
def state_list(df):
    States = df['State_name'].unique().tolist()
    States.sort()
    States.insert(0, 'Overall')
    return States


# =============================================FOR DISTRICT=================================================

def district_list(df):
    Districts = df['District_name'].unique().tolist()
    Districts.sort()
    Districts.insert(0, 'Overall')
    return Districts

Dist_name = df.groupby('District_name').Population.sum().sort_values(ascending = False)
Dist_name = pd.DataFrame(Dist_name, index=None).reset_index()
Dist_name.set_index('District_name').style.format(thousands=",")   


def fetch_district_data(district):
    if district == 'Overall':
        temp_df = Dist_name
    else:
        temp_df = Dist_name[Dist_name['District_name'] == district]   
        
    return temp_df    


def Literacy_dist(district):
    Literacy_dist = df.groupby('District_name')['Literate'].sum()
    Literacy_dist = pd.DataFrame(Literacy_dist).reset_index()
    Literacy_dist.set_index('District_name')

    Literacy_dist['Percentage_of_Literacy'] = round(((Literacy_dist['Literate'] / 
                  Literacy_dist['Literate'].sum()) * 100)*100,2)

    if district == "Overall":
        x = Literacy_dist
    if district != "Overall":
        x = Literacy_dist.loc[Literacy_dist['District_name'] == district]
    return x    


def Worker_plot(district):
    workers = df.groupby('District_name')['Male_Workers','Female_Workers','Cultivator_Workers','Household_Workers'].sum()
    workers = pd.DataFrame(workers).reset_index()
    workers.set_index('District_name')
  
    x = workers.loc[workers['District_name'] == district]

    return x

# ===========================================FOR OVERALL ANALYSIS==============================================

def Worker_State_plot(val):
    workers_state = df.groupby('State_name')['Male_Workers','Female_Workers','Cultivator_Workers','Household_Workers'].sum()
    workers_state = pd.DataFrame(workers_state).reset_index()
    workers_state.set_index('State_name')

    fig1 = px.bar(workers_state, x="State_name", y="Male_Workers",text_auto='.2s',title="Total Male Workers per State")
    fig2 = px.bar(workers_state, x="State_name", y="Female_Workers",text_auto='.2s',title="Total Female Workers per State")
    fig3 = px.bar(workers_state, x="State_name", y="Cultivator_Workers",text_auto='.2s',title="Total Cultivator Workers per State")
    fig4 = px.bar(workers_state, x="State_name", y="Household_Workers",text_auto='.2s',title="Total Household Workers per State")

    return st.plotly_chart(fig1),st.plotly_chart(fig2),st.plotly_chart(fig3),st.plotly_chart(fig4)    

