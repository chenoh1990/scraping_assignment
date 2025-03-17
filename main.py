from scrapers.gov_news_scraper import NewsSiteScraper


if __name__ == '__main__':

    url = "https://www.gov.il/en/collectors/news"
    scraper = NewsSiteScraper(url)
    scraper.scrape_site(url)
    scraper.create_driver()
    print("kek")
