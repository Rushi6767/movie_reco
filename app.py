from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load the data and similarity matrix
movies_dict = pickle.load(open('movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

@app.route('/')
def home():
    titles = movies['title'].values
    return render_template('index.html', titles=titles)

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_name = request.form.get('movie')
    try:
        movie_index = movies[movies['title'] == movie_name].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommended_movies = [movies.iloc[i[0]].title for i in movies_list]
        return render_template('recommendations.html', 
                             movie_name=movie_name,
                             recommendations=recommended_movies)
    except IndexError:
        return render_template('index.html', 
                             titles=movies['title'].values,
                             error="Movie not found. Please select another.")

if __name__ == '__main__':
    app.run(debug=True)