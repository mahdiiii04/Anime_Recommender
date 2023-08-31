import pickle
from flask import Flask, render_template, request
import pandas as pd
from recommend import new_rec,replacement, multiple_rec

file = open('anime_data.pickle', 'rb')
dict = pickle.load(file)
anime_data = dict['animes']
anime_df = pd.DataFrame(anime_data, columns=['ID', 'Title', 'Description', 'Genres', 'Episodes', 'Year', 'Image'])

for index, row in anime_df.iterrows():
    if pd.isnull(row["Episodes"]): 
        ep = float(replacement[row["Title"]])
        anime_df.at[index, "Episodes"] = ep


animes_names = list(anime_df["Title"])
animes_ids = list(anime_df["ID"])
animes_list = []
for i in range(len(animes_names)):
    animes_list.append({
        'id' : animes_ids[i],
        'name' : animes_names[i]
    })


app = Flask(__name__)

chosen_animes = []

@app.route('/', methods=["POST", "GET"])
def index():
    chosen_animes.clear()
    return render_template('index.html', names=animes_list, chosen=[])


@app.route('/adding', methods=['POST'])
def add():
    anime_name = request.form.get('Anime')
    anime_id = anime_df[anime_df["Title"] == anime_name]["ID"].values[0]
    anime_img = anime_df[anime_df["Title"] == anime_name]["Image"].values[0]
    if not any(anime['id'] == anime_id for anime in chosen_animes):        
        chosen_animes.append({
            'id' : anime_id,
            'image' : anime_img
        })
    return render_template('index.html', names=animes_list, chosen=chosen_animes)

@app.route('/deleting', methods=["POST", "GET"])
def delete():    
    id = request.form.get('ID')
    anime_img = anime_df[anime_df["ID"] == id]["Image"].values[0]
    chosen_animes.remove({
        'id' : id,
        'image' : anime_img
    })
    return render_template('index.html', names=animes_list, chosen=chosen_animes)


@app.route('/recommend_anime', methods=['POST'])
def recommend_anime():
    rec_animes = multiple_rec(list(anime['id'] for anime in chosen_animes), 10)
    recommended = [] 
    for anime in rec_animes:
        row = anime_df[anime_df["ID"] == anime]
        recommended.append({
            'title' : row['Title'].values[0],
            'image' : row['Image'].values[0],
            'episodes' : int(row['Episodes'].values[0]),
            'year' : row['Year'].values[0],
            'description' : row['Description'].values[0]
        })
    return render_template('index.html', names=animes_list, recommended=recommended, chosen=[])

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
