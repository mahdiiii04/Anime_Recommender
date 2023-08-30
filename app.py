import pickle
from flask import Flask, render_template, request
import pandas as pd
from recommend import new_rec,replacement

file = open('anime_data.pickle', 'rb')
dict = pickle.load(file)
anime_data = dict['animes']
anime_df = pd.DataFrame(anime_data, columns=['ID', 'Title', 'Description', 'Genres', 'Episodes', 'Year', 'Image'])

for index, row in anime_df.iterrows():
    if pd.isnull(row["Episodes"]): 
        ep = float(replacement[row["Title"]])
        anime_df.at[index, "Episodes"] = ep


anime_names = list(anime_df["Title"])


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', names=anime_names)


@app.route('/recommend_anime', methods=['POST'])
def recommend_anime():
    anime_name = request.form.get('Anime')
    anime_id = anime_df[anime_df["Title"] == anime_name]["ID"].values[0]
    recommended = []
    rec_animes = new_rec(anime_id, 10)
    for id in rec_animes:
        row = anime_df[anime_df['ID'] == id]
        new_anime = {
            'title' : row['Title'].values[0],
            'image' : row['Image'].values[0],
            'episodes' : int(row['Episodes'].values[0]),
            'year' : row['Year'].values[0],
            'description' : row['Description'].values[0]
        }
        recommended.append(new_anime)
    return render_template('index.html', names=anime_names, recommended=recommended)

if __name__ == '__main__':
    app.run(debug=True)