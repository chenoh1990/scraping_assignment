# from scrapers.news.gov_news_scraper import NewsSiteScraper
# from scrapers.paneco.paneco_whiskey_scraper import PanecoWhiskeyScraper
from bots.telegram.telegram_bot import TelegramBot
if __name__ == '__main__':

    # url = "https://www.gov.il/en/collectors/news"
    #
    # scraper = NewsSiteScraper(url)
    # # scraper.create_driver()
    # scraper.scrape_site(url)

    # url = "https://www.paneco.co.il/whiskey"
    #
    # scraper = PanecoWhiskeyScraper(url)
    # scraper.scrape_site(url)

    bot = TelegramBot()
    bot.run()
