import streamlit as st
import pandas as pd
from Recommender import Recommender
import networkx as nx
import plotly.graph_objects as go

def setup_widgets(users):
    with st.form("config"):
        with st.sidebar:
            active_user = st.selectbox(
                'Select a user to start:',
                users
            )
            submitted = st.form_submit_button("GO")
            if submitted:
                return active_user

def axes_layout_option():
    dict_layout = {
        "showline": True,
        "linecolor": "black",
        "gridcolor": "LightGray",
        "mirror": True,
        "title_font_size": 14,
        "ticks": "outside",
    }
    return dict_layout

def setup_page_config():
    st.set_page_config(
        page_title="Anime recommender system",
        layout="wide",
        initial_sidebar_state="expanded",
    )

@st.cache(allow_output_mutation=True)
def read_data():
    # read data
    ual = pd.read_csv('anime_data/animelists_cleaned.csv')
    animes = pd.read_csv('anime_data/anime_cleaned.csv')
    users = pd.read_csv('anime_data/users_cleaned.csv')
    
    # filter data
    usernames = ual['username'].value_counts()[:5].index.tolist() # select top 5 users with most activities
    ual = ual.loc[ual['username'].isin(usernames)]
    users = users.loc[users['username'].isin(usernames)]
    animes = animes.loc[animes['anime_id'].isin(ual['anime_id'].values)]
    return animes, users, ual

def run_plot_recs(animes, recs):
    st.markdown("""---""")
    recommendations = animes.loc[animes['anime_id'].isin([aid for aid,_ in recs])]
    fig = go.Figure(data=[go.Table(
        header=dict(values=['title','title_japanese','source','type','studio','genre','aired_from_year'],
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[recommendations.title, recommendations.title_japanese, 
                            recommendations.source, recommendations.type, 
                            recommendations.studio, recommendations.genre, recommendations.aired_from_year],
                fill_color='lavender',
                align='left'))
    ])
    fig.update_layout(height=2000)
    fig.update_layout(width=1200)
    st.write(fig)

def main():
    setup_page_config()
    st.title("Anime recommender system")
    animes, users, ual = read_data()

    rs = Recommender()
    damping_factor = 0.95
    rs.build_graph(users, animes, ual)
    print(nx.info(rs.graph))
    active_user = setup_widgets(rs.users)

    if active_user:
        recs = rs.run_user(active_user, damping_factor)
        st.header('Top 5 recommendations for %s'%(active_user))
        run_plot_recs(animes, recs)


if __name__ == "__main__":
    main()