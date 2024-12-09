# movie_data_fetcher/tmdb_fetcher/__init__.py

import pandas as pd
import os
from .data_retriever import get_tmdb_data

def get_tmdb_csv():
    """Convert TMDB data to CSV"""
    # Create data directory if needed
    if not os.path.exists("TMDB_data"):
        os.makedirs("TMDB_data")
    
    # Get data from retriever
    all_results = get_tmdb_data()
    
    # Save to CSV
    df = pd.DataFrame(all_results)
    output_file = "TMDB_data/tmdb_all_media.csv"
    df.to_csv(output_file, index=False)
    return output_file