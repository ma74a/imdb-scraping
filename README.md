This script scrapes the IMDb top movies page for movie details and images. It saves the movie details (name, year, rating) in a CSV file and downloads the movie images to a specified directory.
Requirements

    Python 3.11
    requests library
    beautifulsoup4 library
    lxml library
    os library
    csv library

You can install the required libraries using pip:

bash

pip install requests beautifulsoup4 lxml

Usage

    Clone the repository or download the script.
    Ensure all required libraries are installed.
    Run the script using Python.

bash

python3 movies.py

The script will:

    Scrape the IMDb top movies page.
    Save movie details (name, year, rating) to movies.csv.
    Download movie images and save them to a directory named best_movies_imgs.
