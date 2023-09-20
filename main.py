import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class RealEstateScraper:
    def __init__(self, url):
        self.url = url

    def scrape_data(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        listings = soup.find_all('div', class_='property-listing')

        data = pd.DataFrame(columns=['Title', 'Price', 'Location', 'Amenities'])

        for listing in listings:
            title = listing.find('h2').text.strip()
            price = listing.find('span', class_='price').text.strip()
            location = listing.find('div', class_='location').text.strip()
            amenities = ', '.join([amenity.text.strip() for amenity in listing.find_all('span', class_='amenity')])

            data = data.append({'Title': title, 'Price': price, 'Location': location, 'Amenities': amenities},
                               ignore_index=True)

        return data


class RealEstateAnalyzer:
    def __init__(self, data):
        self.data = data

    def preprocess_data(self):
        self.data = self.data.dropna()
        self.data['Price'] = self.data['Price'].str.replace('[^\d.]', '').astype(float)

    def visualize_data(self):
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(12, 6))
        sns.barplot(data=self.data, x='Location', y='Price')
        plt.xticks(rotation=90)
        plt.xlabel('Location')
        plt.ylabel('Price')
        plt.title('Average Property Price by Location')
        plt.show()

    def analyze_trends(self):
        average_price = self.data['Price'].mean()
        median_price = self.data['Price'].median()
        max_price = self.data['Price'].max()
        min_price = self.data['Price'].min()

        print(f'Average Price: ${average_price:.2f}')
        print(f'Median Price: ${median_price:.2f}')
        print(f'Maximum Price: ${max_price:.2f}')
        print(f'Minimum Price: ${min_price:.2f}')


# Web scraping
url = 'https://www.example.com/real-estate'
scraper = RealEstateScraper(url)
data = scraper.scrape_data()

# Data preprocessing
analyzer = RealEstateAnalyzer(data)
analyzer.preprocess_data()

# Data visualization
analyzer.visualize_data()

# Trend analysis
analyzer.analyze_trends()