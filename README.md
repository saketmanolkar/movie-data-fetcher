# Movie Data Fetcher

A Python package to fetch movie data from BoxOffice API and TMDB.

# Installation

## Usage

from tmdb_fetcher import get_tmdb_csv
from boxoffice_fetcher import get_boxoffice_csv,get_theatrical_csv


## Output Files

### theatrical_releases.csv
Contains current theatrical releases with:
- Title
- Distributor
- Daily Gross
- To Date Earnings
- Days Released
- Theater Count
- Movie Poster URL

### combined_monthly_earnings.csv
Contains monthly earnings for major distributors:
- Universal Pictures
- Warner Bros.
- Paramount Pictures
- Sony Pictures
- Disney
- And more...

### tmdb_all_media.csv
Contains TMDB movie data including:
- Movie details
- Ratings
- Release information