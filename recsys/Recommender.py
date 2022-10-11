import networkx as nx
import pandas as pd
import numpy as np
from random import sample
from utils import *

class Recommender:
    def __init__(self):
        self.graph = None
        self.users = None
        self.ratings = None
        self.animes = None

    def build_graph(self, users, animes, ual):
        B = nx.DiGraph()
        # Add nodes
        B.add_nodes_from(animes['anime_id'].unique(),node_type='anime')         
        B.add_nodes_from(users['username'].unique(),node_type='user')
        
        all_genres = set()
        for anime_id, genre_list in animes[['anime_id','genre']].values:
            if pd.notnull(genre_list):
                genres = genre_list.split(',')
                for genre in genres:
                    genre = genre.strip()
                    if genre not in all_genres:
                        all_genres.add(genre)
                        B.add_node(genre,node_type='genre')
                    B.add_edge(anime_id,genre)
        
        all_studios = set()
        for anime_id, studio_list in animes[['anime_id','studio']].values:
            if pd.notnull(studio_list):
                studios = studio_list.split(',')
                for studio in studios:
                    studio = studio.strip()
                    if studio not in all_studios:
                        all_studios.add(studio)
                        B.add_node(studio,node_type='studio')
                    B.add_edge(anime_id,studio)

        # Season, assume people would be interested in animes that were in the same period as they liked/rated highly
        # reduce the bias brought by popularity
        lookup = {'Winter':'1','Spring':'2','Summer':'3','Fall':'4'}
        season_lookup = {season:'-'.join([season.split()[1], lookup[season.split()[0]]]) for season in animes['premiered'].unique() if pd.notnull(season)}
        sorted_season_list = sorted(list(season_lookup.values())) # chronological sequence of seasons
        for i, season_code in enumerate(sorted_season_list):
            B.add_node(season_code, node_type='season')
            if i>=1:
                B.add_edge(season_code, sorted_season_list[i-1]) # connect consequent seasons together
        for anime_id, season in animes[['anime_id','premiered']].values:
            if pd.notnull(season):
                B.add_edge(anime_id,season_lookup[season]) # edges that connect anime to its season

        ual['score_normalized'] = ual.groupby('username')['my_score'].transform(lambda x: (x - x.mean()) / x.std())
        for user, anime_id, score, score_norm in ual[['username','anime_id','my_score','score_normalized']].values:
            if score>=5 and anime_id in list(B.nodes):
                B.add_edge(user, anime_id, weight=score_norm+1)

        B.remove_nodes_from(list(nx.isolates(B))) # remove isolated nodes as they don't produce recommendations

        self.graph = B
        self.users = [n for n,v in B.nodes(data=True) if v['node_type'] == 'user']
        self.animes = [n for n,v in B.nodes(data=True) if v['node_type'] == 'anime']
        self.ratings = ual

    def run_user(self, active_user, damping_factor):
        ppr_values = nx.pagerank(G=self.graph, alpha=damping_factor, max_iter=100000, personalization={active_user:1.0}, weight='weight')
        # print('previous watched animes',self.ratings.loc[self.ratings['username']==active_user,'anime_id'].values)
        anime_ppr_values = {node:value for node,value in ppr_values.items() if nx.get_node_attributes(self.graph, "node_type")[node]=='anime' 
                            and node not in self.ratings.loc[self.ratings['username']==active_user,'anime_id'].values}
        # print('candidate set size',len(anime_ppr_values))

        return topn_from_dict(anime_ppr_values, 5)

if __name__ == '__main__':
    # read data
    ual = pd.read_csv('anime_data/animelists_cleaned.csv')
    animes = pd.read_csv('anime_data/anime_cleaned.csv')
    users = pd.read_csv('anime_data/users_cleaned.csv')
    
    # filter data
    animes = animes.loc[animes['aired_from_year']>=2000] # we only focus on animes after 2000
    users = users.sample(n=500) # randomly select 500 users
    ual = ual.loc[ual['username'].isin(users.username.unique())].dropna(subset=['username','anime_id','my_score'])

    rs = Recommender()
    rs.build_graph(users, animes, ual)
    active_user = sample(rs.users, 1)[0] # randomly select a user for test
    damping_factor = 0.85
    recommendations = rs.run_user(active_user, damping_factor)

    print(animes.loc[animes['anime_id'].isin([aid for aid,_ in recommendations])])