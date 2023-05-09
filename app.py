import streamlit as st
import json
from scraper.scraper import Scraper
from scraper import utils


#st.title(("LinkedIn Assistant"))


add_selectbox = st.sidebar.selectbox(
    'Choose a Desired Option',
    ('First Time User',
     'Remake Dataset',
      'Start Querying')
)

if (add_selectbox == 'First Time User') or (add_selectbox == 'Remake Dataset'):
    st.text_input("Your email", key="email")
    st.text_input("Password", key="pwd",type="password")
    email = st.session_state.email
    pwd = st.session_state.pwd
    if st.button("Run"):
        with st.spinner('Accessing Profile'):
            profile_url,driver = utils.access_profile(email,pwd)
        st.success("Profile Accessed")
        ## Create a Scraper object with the profile URL
        with st.spinner('Scrapping Post of {}'.format(profile_url)):
            scraper = Scraper(profile_url)
            ## Scrape the posts
            data, conn_names, driver = scraper.scrape_posts(driver)
        st.success("Done")
        ## 
        #del conn_names[profile_url]
        #scraper.scrape_conn_posts(driver,conn_names)




elif add_selectbox == 'Start Querying':
    st.text_input("Enter your query", key="query")
    if st.button("Query"):
        pass


## if user want to make dataset then take credentials
#if st.checkbox('First Time User / Remake dataset'):

    # You can access the value at any point with:
#    st.session_state.email

#if st.checkbox('Start Querying'):
#    st.text_input("Enter your query", key="query")

    # You can access the value at any point with:
#    st.session_state.query


#left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
#left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
#with right_column:
#    chosen = st.radio(
#        'Sorting hat',
#        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
#    st.write(f"You are in {chosen} house!") 