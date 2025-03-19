from factories.scraper_factory import ScraperFactory

if __name__ == '__main__':

    """ please select the appropriate scraper by removing the relevant variables from the comment. """

    url = "https://www.gov.il/en/collectors/news"
    scraper_type = "news"

    # url = "https://www.paneco.co.il/whiskey"
    # scraper_type = "paneco"

    try:
        scraper = ScraperFactory.create_scraper(scraper_type, url)
        scraper.scrape_site(url)

    except Exception as ex:
        print(f"failed to initialize the scraper. error: {ex}")
