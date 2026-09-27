import feedparser
import re
from utils import is_recent


RSS_FEEDS = {
    "Indian Stock Market":
        "https://news.google.com/rss/search?q=Indian+stock+market+NSE+BSE&hl=en-IN&gl=IN&ceid=IN:en",

    "Indian Companies":
        "https://news.google.com/rss/search?q=Indian+companies+stocks+earnings+orders&hl=en-IN&gl=IN&ceid=IN:en",

    "RBI SEBI Economy":
        "https://news.google.com/rss/search?q=RBI+SEBI+India+economy+markets&hl=en-IN&gl=IN&ceid=IN:en",

    "Indian Corporate Actions":
        "https://news.google.com/rss/search?q=India+stocks+IPO+acquisition+merger+fundraising+order&hl=en-IN&gl=IN&ceid=IN:en",

    "Indian Sectors":
        "https://news.google.com/rss/search?q=India+banking+IT+pharma+auto+energy+stocks&hl=en-IN&gl=IN&ceid=IN:en",
}


# High-impact keywords
HIGH_PRIORITY = [
    "rbi",
    "sebi",
    "interest rate",
    "repo rate",
    "inflation",
    "earnings",
    "profit",
    "loss",
    "revenue",
    "results",
    "order",
    "contract",
    "acquisition",
    "merger",
    "ipo",
    "listing",
    "fundraising",
    "stake",
    "dividend",
    "buyback",
    "default",
    "fraud",
    "regulatory",
    "penalty",
    "approval",
    "government",
    "tariff",
    "ban",
    "policy",
]


MEDIUM_PRIORITY = [
    "nifty",
    "sensex",
    "bank nifty",
    "vix",
    "fii",
    "dii",
    "rupee",
    "crude",
    "oil",
    "gold",
    "it stocks",
    "banking",
    "pharma",
    "auto",
    "energy",
]


# Words that usually indicate low-value commentary
LOW_VALUE = [
    "technical analysis",
    "stocks to buy",
    "stocks to sell",
    "best stocks",
    "multibagger",
    "penny stocks",
    "intraday picks",
    "trading strategy",
    "market prediction",
]


def clean_title(title):
    """Clean Google News RSS headline."""

    title = re.sub(r"\s+", " ", title)
    title = title.strip()

    return title


def normalize_title(title):
    """Create a simplified title for duplicate detection."""

    title = title.lower()

    # Remove punctuation
    title = re.sub(r"[^a-z0-9\s]", " ", title)

    # Remove common news words
    stop_words = {
        "india",
        "indian",
        "stock",
        "stocks",
        "market",
        "markets",
        "shares",
        "share",
        "today",
        "latest",
        "news",
    }

    words = [
        word
        for word in title.split()
        if word not in stop_words
    ]

    return " ".join(words)


def calculate_relevance(title, source):

    text = title.lower()

    score = 0

    for keyword in HIGH_PRIORITY:
        if keyword in text:
            score += 3

    for keyword in MEDIUM_PRIORITY:
        if keyword in text:
            score += 1

    # Prefer reliable financial/news sources
    trusted_sources = [
        "reuters",
        "economic times",
        "moneycontrol",
        "livemint",
        "business standard",
        "businessline",
        "cnbc",
    ]

    for trusted in trusted_sources:
        if trusted in source.lower():
            score += 2

    # Penalize low-value content
    for keyword in LOW_VALUE:
        if keyword in text:
            score -= 4

    return score


def is_low_value(title):

    text = title.lower()

    for keyword in LOW_VALUE:
        if keyword in text:
            return True

    return False


def remove_similar_articles(news):

    selected = []
    seen_signatures = set()

    for article in news:

        signature = normalize_title(article["title"])

        # Exact normalized duplicate
        if signature in seen_signatures:
            continue

        # Compare important words with previous stories
        current_words = set(signature.split())

        duplicate = False

        for previous in selected:

            previous_words = set(
                normalize_title(previous["title"]).split()
            )

            if not current_words or not previous_words:
                continue

            overlap = len(
                current_words & previous_words
            ) / max(
                1,
                min(len(current_words), len(previous_words))
            )

            # If most important words overlap,
            # treat as same story.
            if overlap >= 0.75:
                duplicate = True
                break

        if not duplicate:
            selected.append(article)
            seen_signatures.add(signature)

    return selected


def get_news():

    all_news = []

    print("\nCollecting news...")

    for category, url in RSS_FEEDS.items():

        feed = feedparser.parse(url)

        print(
            f"{category}: "
            f"{len(feed.entries)} articles found"
        )

        for entry in feed.entries:

            title = clean_title(
                entry.get("title", "")
            )

            published = entry.get(
                "published",
                entry.get("updated", "")
            )

            source = entry.get(
                "source",
                {}
            )

            if isinstance(source, dict):
                source_name = source.get(
                    "title",
                    ""
                )
            else:
                source_name = str(source)

            # Ignore empty headlines
            if not title:
                continue

            # Keep recent stories only
            if not is_recent(
                published,
                hours=36
            ):
                continue

            # Ignore low-value trading content
            if is_low_value(title):
                continue

            score = calculate_relevance(
                title,
                source_name
            )

            all_news.append({
                "category": category,
                "title": title,
                "published": published,
                "source": source_name,
                "link": entry.get("link", ""),
                "relevance_score": score,
            })

    print(
        f"\nRecent usable articles: "
        f"{len(all_news)}"
    )

    # Remove similar stories
    all_news = remove_similar_articles(
        all_news
    )

    print(
        f"After duplicate filtering: "
        f"{len(all_news)}"
    )

    # Highest relevance first
    all_news.sort(
        key=lambda x: x["relevance_score"],
        reverse=True
    )

    # Keep only the best 15
    all_news = all_news[:15]

    print(
        f"Final articles sent to AI: "
        f"{len(all_news)}"
    )

    return all_news


if __name__ == "__main__":

    news = get_news()

    print("\n" + "=" * 70)
    print("🔥 SELECTED MARKET NEWS")
    print("=" * 70)

    for i, article in enumerate(news, 1):

        print(f"\n{i}. {article['title']}")
        print(f"   Category: {article['category']}")
        print(f"   Source: {article['source']}")
        print(f"   Score: {article['relevance_score']}")
        print(f"   Link: {article['link']}")