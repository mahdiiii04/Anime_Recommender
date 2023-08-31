import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from collections import Counter


file = open('anime_data.pickle', 'rb')
dict = pickle.load(file)
anime_data = dict['animes']

df = pd.DataFrame(anime_data, columns=['ID', 'Title', 'Description', 'Genres', 'Episodes', 'Year', 'Image'])

replacement = {
    "One Piece" : 1073,
    "Detective Conan": 1123,
    "Tate no Yuusha no Nariagari Season 3" : 13,
    "High School DxD OVA" : 2,
    "Kokoro Connect: Michi Random" : 4
}

for index, row in df.iterrows():
    if pd.isnull(row["Episodes"]): 
        ep = float(replacement[row["Title"]])
        df.at[index, "Episodes"] = ep

id_to_index = {}
index_to_id = {}
ids = list(df['ID'])
for counter in range(len(ids)):
    id_to_index[ids[counter]] = counter
for counter in range(len(ids)):
    index_to_id[counter] = ids[counter]


def process_genres(genre_string):
    genres_list = genre_string.split(',')
    formatted_genres = ' '.join(genres_list)
    return formatted_genres

new_df = df["Description"] + df["Genres"].apply(process_genres)
vecter = TfidfVectorizer(stop_words='english')
features_matrix = vecter.fit_transform(new_df)
new_similarity = cosine_similarity(features_matrix)

def new_rec(id, num):
    index = id_to_index[str(id)]
    similarity_array = np.argsort(new_similarity[index])[::-1][1:]
    rec_ids = []
    for index in similarity_array:
        rec_ids.append(index_to_id[index])
        if len(rec_ids) >= num:
            break
    return rec_ids

def multiple_rec(ids, num):
    combined = []
    for id in ids:
        recommended = new_rec(id, 50)
        for rec_id in recommended:
            combined.append(rec_id)
    id_counter = Counter(combined)
    mci = id_counter.most_common()
    for c in mci:
        if c[0] in ids:
            mci.remove(c)
    rec = list(c[0] for c in mci[:num])
    return rec
    


