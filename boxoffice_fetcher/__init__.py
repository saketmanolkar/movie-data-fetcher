# movie_data_fetcher/boxoffice_fetcher/__init__.py

import os
import pandas as pd
from .data_retriever import BoxOfficeRetriever

def get_boxoffice_csv():
    """Get combined box office data CSV"""
    # Create data directory
    if not os.path.exists("BoxOffice_data"):
        os.makedirs("BoxOffice_data")
    
    # Get and save data
    retriever = BoxOfficeRetriever()
    combined_df = retriever.get_combined_data()
    
    output_file = "BoxOffice_data/combined_monthly_earnings.csv"
    combined_df.to_csv(output_file, index=False)
    print(f"\nData saved to: {output_file}")
    return output_file

def get_theatrical_csv():
    """Get theatrical releases with posters as CSV"""
    # Create data directory
    if not os.path.exists("BoxOffice_data"):
        os.makedirs("BoxOffice_data")
    
    print("Initializing BoxOffice retriever...")
    retriever = BoxOfficeRetriever()
    
    print("\nGetting theatrical data...")
    theatrical_df = retriever.get_theatrical_data()
    
    if theatrical_df is not None:
        output_file = "BoxOffice_data/theatrical_releases.csv"
        theatrical_df.to_csv(output_file, index=False)
        print(f"\nData saved to: {output_file}")
        return output_file
    
    print("Failed to get theatrical data")
    return None