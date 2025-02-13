## *DATAFRAMES AND PACKAGES*

# import packages
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
pio.renderers.default='browser'
import streamlit as st 
from streamlit_dynamic_filters import DynamicFilters
import plotly.graph_objects as go



##################### STREAMLIT  INFOS
# https://docs.streamlit.io/develop
# look in API reference

##################### STREAMLIT  LIBRARIES
### pour obtenir l'exemple installer :
# streamlit
# streamlit_dynamic_filters

### un autre intéressant : 
# streamlit-extras (custom metric cards)
	# https://extras.streamlit.app/
	# https://arnaudmiribel.github.io/streamlit-extras/extras/metric_cards/

##################### RUN STREAMLIT  
# save all the files in the working directory folder
# run streamlit from Anaconda prompt 
    # locate your working directory (cd + space + past the path)
        # write: C:\cd yourpath\wd
        # obtain: C:\cd yourpath\wd
    # execute the notebook M2_streamlit.py
        # write: streamlit run M2_streamlit.py


##################### DATA
# open and rename the dataframe FB.csv 
FB = pd.read_csv("FB_NA_handled.csv", sep=",", header=0)
FB = FB.dropna()

##################### PAGE
st.set_page_config(layout="wide")


##################### SIDE BAR

# Organize the side bar  

# name your side bar 
st.sidebar.title("Content")

# name 3 pages
pages = ["Project description", "Main results", "Dashboard"]

# create navigation among your pages
page = st.sidebar.radio("Go to page :", pages)

# build page n°0
if page == pages[0] : 
    
    # add text with st.write() note that # specifies header 1 ## header 2 ### header 3 
    st.write("# Project description") 
    
    st.write("## Introduce your missions to your customer")
    
    st.write("### another level for text")
       
    
    if st.checkbox("Display dataframe") : 
        st.dataframe(FB)
        
    if st.checkbox("Display variables' names") : 
        display = list(FB.columns.values)
        st.write(display)
        
        
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("comment.jpg")

    with col2:
        st.image("fb.jpg")

    with col3:
        st.image("like.jpg")

##################### PAGE 1

elif page == pages[1]:
    st.write("### Main results")
    
    # transform numerical variable to categorical variable before forming crosstab 
    FB["share_2cat"] = pd.cut(FB["share"], bins = [0, 27, 790], precision = 0, right = True, labels = ["Few shares", "Lot shares"], include_lowest=True)
    # cross-tab
    crosstab_4 = pd.crosstab(FB["Type"], FB["share_2cat"])
    st.table(crosstab_4)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("comment.jpg")

    with col2:
            st.image("comment.jpg")

    with col3:
        st.image("like.jpg")
        
    st.write("1. your analysis + 2. your interpretation + 3. your recommandations")

    # create object in your notebook without any action in your wep app
    group = FB.groupby("Post Weekday")["Lifetime Post Total Reach"].mean()
    # display your object thanks to a streamlit function
    st.table(group)

    hist1 = px.histogram(FB, x="like")
    st.plotly_chart(hist1)

    pie2 = px.pie(FB, values="like", names="Type", color_discrete_sequence = px.colors.sequential.Mint, hole=0.5)
    st.plotly_chart(pie2)

    like_focus = FB[(FB["like"] <2000)]
    scatter3 = px.scatter(like_focus, y="like",x="comment", facet_col = "Paid", color="Category", trendline="ols")
    st.plotly_chart(scatter3)
    

    
##################### PAGE 2
elif page == pages[2]:
    
######## create container n°1 (filter data)
    part1 = st.container()

    with part1:
        st.write("Your dashboard title")
        
        # Add text for viewers
        st.sidebar.header("Select a filter")
        
        # Select variables from df to filter data    
        dynamic_filters = DynamicFilters(FB, filters=["Category", "Type", "Paid"])
        
        # Display the filters in your app. below the previous text
        dynamic_filters.display_filters(location="sidebar")
        
        # Display the filtered dataframe (depending on selected filtered)
        if st.checkbox("Display filtered dataframe") : 
            dynamic_filters.display_df()
        
        # Assign a filtered dataframe object (to use for analyses)
        FB_filtered = dynamic_filters.filter_df()
        
    
######## create container n°2 (KPI)
    part2 = st.container()

    with part2:
        # create and name six columns
        kpi1, image1, kpi2, image2, kpi3, image3  = st.columns(6)
        
        # compute your KPI
        metric1 = np.mean(FB_filtered["like"])
        metric2 = np.mean(FB_filtered["share"])
        metric3 = np.mean(FB_filtered["comment"])
                      
        # display your columns (each image is related to one KPI)
        
        kpi1.metric(label = "Mean of like", value = int(metric1))
        image1.image("like2.png", width=100)
        
        kpi2.metric(label = "Mean of share", value = int(metric2))
        image2.image("share.png", width=100)
        
        kpi3.metric(label = "Mean of comment", value = int(metric3))
        image3.image("comment.jpg", width=100)
        
 
######## create container n°3 (chart and table)
    part3 = st.container()

    with part3:
        # create two columns
        # set columns, and columns' width
        # it is relative width: 100% for one unic column
        col1, col2 = st.columns([0.4, 0.6])

        with col1:
            # create a pie chart to study filtered data (nb share / day)
            pie2 = px.pie(FB_filtered, values="share", names="Post Weekday", color_discrete_sequence = px.colors.sequential.Mint, hole=0.5)
            # display the pie chart in your dashboard
            st.plotly_chart(pie2) 
      
        with col2:
    
            # build a gauge chart
            # 1. set the value to display from filtered data 
            value = int(np.round(FB_filtered["comment"].max()))
            # 2. set the background of the gauge 
            gauge1 = go.Figure(go.Indicator(
                mode="gauge+number",
                value=value,
                title={'text': "Max of comment"},
                gauge={'axis': {'range': [FB["comment"].min() , FB["comment"].max()]}, # min and max among the whole df
                    'bar': {'color': "#FF8C00"},
                    }
            ))
            # 3. set the size of the gauge
            gauge1.update_layout(height=350)
            
            # display the gauge chart in your dashboard
            st.plotly_chart(gauge1, use_container_width=True)



     
        
        
        

