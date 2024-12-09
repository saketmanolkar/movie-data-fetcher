# movie_data_fetcher/boxoffice_fetcher/data_retriever.py

from boxoffice_api import BoxOffice
from datetime import datetime, timedelta
import pandas as pd
import time
import requests
from collections import defaultdict

class BoxOfficeRetriever:
    def __init__(self):
        self.box_office = BoxOffice()
        self.tmdb_api_key = "ebe22d808571308fd8e1de62e03b2040"
        self.distributors = {
            "Warner Bros.",
            "Universal Pictures",
            "Paramount Pictures",
            "Sony Pictures Releasing",
            "Walt Disney Studios Motion Pictures",
            "20th Century Studios",
            "Lionsgate",
            "A24",
            "IFC Films",
            "Focus Features"
        }
        self.months = {
            1: "January", 2: "February", 3: "March", 4: "April",
            5: "May", 6: "June", 7: "July", 8: "August",
            9: "September", 10: "October", 11: "November", 12: "December"
        }

    def _get_distributor_earnings(self):
        """Get earnings for major distributors"""
        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month
        
        rows = []
        headers = ['Distributor']
        
        # Generate headers
        for year in range(current_year - 2, current_year + 1):
            for month in self.months.values():
                headers.append(f"{month} {year}")
        
        # Get data for each distributor
        total_distributors = len(self.distributors)
        for idx, distributor in enumerate(self.distributors, 1):
            print(f"\nProcessing {distributor} ({idx}/{total_distributors})...")
            row = [distributor]
            for year in range(current_year - 2, current_year + 1):
                months = range(1, 13) if year != current_year else range(1, current_month + 1)
                for month in months:
                    try:
                        print(f"  Fetching {self.months[month]} {year}...", end='', flush=True)
                        monthly_data = self.box_office.get_monthly(year=year, month=month)
                        if monthly_data:
                            total = sum(
                                float(movie['Gross'].replace('$', '').replace(',', ''))
                                for movie in monthly_data
                                if movie['Distributor'] == distributor
                            )
                            row.append(f"${total:,.2f}")
                            print(" ✓")
                        else:
                            row.append("$0.00")
                            print(" (no data)")
                        time.sleep(1)
                    except Exception as e:
                        print(f" Error: {str(e)}")
                        row.append("$0.00")
                        time.sleep(2)
            rows.append(row)
        
        return pd.DataFrame(rows, columns=headers)

    def _get_total_earnings(self):
        """Get total industry earnings"""
        current_date = datetime.now()
        current_year = current_date.year
        current_month = current_date.month
        
        row = ['Total Industry Earnings']
        headers = ['Distributor']
        
        # Generate headers and get data
        for year in range(current_year - 2, current_year + 1):
            months = range(1, 13) if year != current_year else range(1, current_month + 1)
            for month in months:
                month_name = self.months[month]
                headers.append(f"{month_name} {year}")
                try:
                    print(f"Fetching total for {month_name} {year}...", end='', flush=True)
                    monthly_data = self.box_office.get_monthly(year=year, month=month)
                    if monthly_data:
                        total = sum(
                            float(movie['Gross'].replace('$', '').replace(',', ''))
                            for movie in monthly_data
                        )
                        row.append(f"${total:,.2f}")
                        print(" ✓")
                    else:
                        row.append("$0.00")
                        print(" (no data)")
                    time.sleep(1)
                except Exception as e:
                    print(f" Error: {str(e)}")
                    row.append("$0.00")
                    time.sleep(2)
        
        return pd.DataFrame([row], columns=headers)

    def get_combined_data(self):
        """Get combined box office data"""
        print("Fetching distributor earnings...")
        distributor_df = self._get_distributor_earnings()
        
        print("\nFetching total industry earnings...")
        total_df = self._get_total_earnings()
        
        print("\nCombining data...")
        combined_df = pd.concat([distributor_df, total_df], ignore_index=True)
        
        # Sort to ensure Total Industry is at bottom
        combined_df['sort_key'] = combined_df['Distributor'].apply(
            lambda x: 2 if x == 'Total Industry Earnings' else 1
        )
        combined_df = combined_df.sort_values('sort_key').drop('sort_key', axis=1)
        
        return combined_df.reset_index(drop=True)

    def _get_tmdb_poster_path(self, movie_title):
        """Get poster path from TMDB"""
        search_url = "https://api.themoviedb.org/3/search/movie"
        params = {
            'api_key': self.tmdb_api_key,
            'query': movie_title
        }
        
        try:
            response = requests.get(search_url, params=params)
            if response.status_code == 200:
                results = response.json().get('results', [])
                if results:
                    return results[0].get('poster_path')
        except Exception as e:
            print(f"Error getting poster: {str(e)}")
        return None


    def get_theatrical_data(self):
        """Get current theatrical releases with posters"""
        today = datetime.now()
        yesterday = (today - timedelta(days=1)).strftime('%Y-%m-%d')
        
        try:
            print("Fetching daily box office data...")
            daily_data = self.box_office.get_daily(yesterday)
            
            if daily_data:
                print(f"Found {len(daily_data)} movies in theaters")
                
                theatrical_data = []
                for movie in daily_data:
                    title = movie.get('Title', movie.get('Release', 'Unknown'))
                    print(f"\nProcessing: {title}")
                    
                    # Special handling for re-releases
                    search_title = title.split('2024')[0].strip() if '2024' in title else title
                    poster_path = self._get_tmdb_poster_path(search_title)
                    
                    movie_data = {
                        'Title': title,
                        'Distributor': movie.get('Distributor', 'N/A'),
                        'Daily Gross': movie.get('Daily', movie.get('Gross', '$0')),
                        'Total Gross': movie.get('To Date', '$0'),  # Changed to 'To Date'
                        'Days Released': movie.get('Days Released', '0'),
                        'Theaters': movie.get('Theaters', '0'),
                        'Poster URL': f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "No poster found"
                    }
                    
                    theatrical_data.append(movie_data)
                    print("✓ Added to dataset")
                    
                # Create DataFrame
                df = pd.DataFrame(theatrical_data)
                print("\nCreated DataFrame with columns:", df.columns.tolist())
                return df
                
            else:
                print("No daily data received")
                return None
                
        except Exception as e:
            print(f"Error: {str(e)}")
            if 'daily_data' in locals():
                print("\nRaw data sample:", daily_data[0] if daily_data else "No data")
            return None