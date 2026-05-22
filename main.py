import time
import requests

BOT_TOKEN = "8689029637:AAGZLwew8ra9IacPmTs2bOtf7KQJg-e0oU4"
CHAT_ID = "5785670313"

KEYWORDS = [
    "jesus",
    "ufo",
    "alien",
    "pope",
    "gta",
    "openai",
    "tesla",
    "elon",
    "trump",
    "election",
    "war",
    "fed",
    "rate cut",
    "etf",
    "sec",
    "court",
    "apple",
    "nvidia",
    "release",
    "launch",
    "approve",
    "playstation",
    "xbox"
]

seen_ids = set()

def send_telegram(text):

    try:

        requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            params={
                "chat_id": CHAT_ID,
                "text": text
            },
            timeout=10
        )

    except Exception as e:

        print("Telegram Error:", e)

def interesting(title):

    title = title.lower()

    if "bitcoin up or down" in title:
        return False

    if "btc up or down" in title:
        return False

    if "5m" in title:
        return False

    if "15m" in title:
        return False

    if "30m" in title:
        return False

    if "1h" in title:
        return False

    return any(word in title for word in KEYWORDS)

send_telegram("✅ Polymarket Alert Bot gestartet")

print("Bot läuft...")

while True:

    try:

        url = "https://gamma-api.polymarket.com/markets?closed=false&limit=100&order=createdAt&ascending=false"

        response = requests.get(url, timeout=10)

        markets = response.json()

        for market in markets:

            market_id = str(market.get("id"))

            title = market.get("question", "")

            slug = market.get("slug", "")

            if market_id in seen_ids:
                continue

            seen_ids.add(market_id)

            if title and interesting(title):

                if slug:
                    link = f"https://polymarket.com/event/{slug}"
                else:
                    link = "https://polymarket.com/markets"

                message = (
                    f"🚨 NEW POLYMARKET MARKET\n\n"
                    f"{title}\n\n"
                    f"{link}"
                )

                print("Gefunden:", title)

                send_telegram(message)

    except Exception as e:

        print("ERROR:", e)

    time.sleep(30)
