from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from waitress import serve

app = Flask(__name__)

# Load and preprocess data
def load_data():
    books_df = pd.read_csv('data/books.csv')
    ratings_df = pd.read_csv('data/ratings.csv')
    return books_df, ratings_df

def create_feature_matrix(books_df):
    # Create TF-IDF matrix from book titles and authors
    books_df['features'] = books_df['title'].fillna('') + ' ' + books_df['authors'].fillna('')
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(books_df['features'])
    return tfidf_matrix

def get_recommendations(book_id, books_df, similarity_matrix):
    idx = books_df.index[books_df['book_id'] == book_id][0]
    sim_scores = list(enumerate(similarity_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Get top 5 similar books
    book_indices = [i[0] for i in sim_scores]
    return books_df.iloc[book_indices][['book_id', 'title', 'authors', 'average_rating']]

# Load data when the application starts
try:
    books_df, ratings_df = load_data()
    tfidf_matrix = create_feature_matrix(books_df)
    similarity_matrix = cosine_similarity(tfidf_matrix)
except Exception as e:
    print(f"Error loading data: {e}")
    books_df, ratings_df = None, None
    similarity_matrix = None

@app.route('/')
def home():
    popular_books = books_df.nlargest(10, 'average_rating')[['title', 'authors', 'average_rating']]
    return render_template('index.html', popular_books=popular_books.to_dict('records'))

@app.route('/recommend', methods=['POST'])
def recommend():
    book_id = request.form.get('book_id')
    if not book_id:
        return jsonify({'error': 'No book ID provided'})
    
    try:
        recommendations = get_recommendations(int(book_id), books_df, similarity_matrix)
        return jsonify({'recommendations': recommendations.to_dict('records')})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify({'results': []})
    
    results = books_df[books_df['title'].str.lower().str.contains(query, na=False)]
    return jsonify({'results': results.head(10)[['book_id', 'title', 'authors']].to_dict('records')})

if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'development':
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        serve(app, host='0.0.0.0', port=5000) 