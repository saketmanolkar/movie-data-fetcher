# movie_data_fetcher/tmdb_fetcher/data_retriever.py

import requests
import os

def get_tmdb_data():
    """Get and map TMDB data (1500 entries)"""
    api_key = "ebe22d808571308fd8e1de62e03b2040"
    base_url = "https://api.themoviedb.org/3"
    
    # Language mapping
    language_map = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'ja': 'Japanese',
        'ko': 'Korean',
        'hi': 'Hindi',
        'de': 'German',
        'it': 'Italian',
        'zh': 'Chinese',
        'ru': 'Russian'
    }
    
    # Get genre mapping from TMDB
    genre_response = requests.get(f"{base_url}/genre/movie/list", params={'api_key': api_key})
    genre_map = {genre['id']: genre['name'] for genre in genre_response.json()['genres']}
    
    all_results = []
    for page in range(1, 75):  # 20 pages × 75 = 1500 entries
        params = {
            'api_key': api_key,
            'page': page
        }
        response = requests.get(f"{base_url}/movie/popular", params=params)
        if response.status_code == 200:
            items = response.json()['results']
            for item in items:
                # Map genre IDs to names
                genre_names = [genre_map.get(genre_id, str(genre_id)) for genre_id in item.get('genre_ids', [])]
                genre_names_str = ', '.join(genre_names)
                
                # Map language code to name
                language_name = language_map.get(item.get('original_language'), item.get('original_language'))
                
                filtered_item = {
                    'name': item.get('title'),
                    'genres': genre_names_str,
                    'original_language': language_name,
                    'first_air_date': item.get('release_date'),
                    'media_type': 'movie',
                    'poster_path': item.get('poster_path'),
                    'popularity': item.get('popularity', 0.0)
                }
                all_results.append(filtered_item)
    
    return all_results