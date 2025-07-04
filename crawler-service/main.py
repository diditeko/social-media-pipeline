import asyncio
from scrape import Scraper
from producer import KafkaTweetProducer
from utils import load_accounts_from_file
from decouple import config
from ast import literal_eval
from datetime import datetime, timedelta


KAFKA_TOPIC = config("KAFKA_TOPIC")
KEYWORDS = literal_eval(config("Keywords"))
print(KEYWORDS) # parse stringified list


# Date range: last 7 days
today = datetime.utcnow().date()
seven_days_ago = today - timedelta(days=7)
since = seven_days_ago.strftime("%Y-%m-%d")
until = today.strftime("%Y-%m-%d")

async def run_scraper():
    scraper = Scraper()
    accounts = await load_accounts_from_file(scraper.api)
    producer = KafkaTweetProducer(topic=KAFKA_TOPIC)

    print(f"[+] Using {len(accounts)} valid accounts")
    print(f"[+] Keywords to scrape: {KEYWORDS}")
    print(f"[+] Date range: {since} to {until}")

    for keyword in KEYWORDS:
        print(f"[+] Scraping keyword: {keyword}")
        try:
            # Build search query with date filter embedded in string
            query = f"{keyword} since:{since} until:{until}"
            tweets = await scraper.search(query, limit=1000)

            for tweet in tweets:
                data = {
                    "id": tweet.id,
                    "username": tweet.user.username,
                    "text": tweet.rawContent,
                    "date": str(tweet.date),
                    "keyword": keyword
                }
                producer.send(data)
                print(f"[+] Sent tweet: {data['id']}")
                await asyncio.sleep(0.5)  # Respect rate limits
        except Exception as e:
            print(f"[!] Error scraping {keyword}: {e}")
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(run_scraper())