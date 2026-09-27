import yfinance as yf


SYMBOLS = {
    "Nifty 50": "^NSEI",
    "Sensex": "^BSESN",
    "Bank Nifty": "^NSEBANK",
    "India VIX": "^INDIAVIX",
}


def get_market_data():
    results = {}

    for name, symbol in SYMBOLS.items():
        try:
            data = yf.Ticker(symbol).history(period="5d")

            if data.empty:
                results[name] = {"status": "No data"}
                continue

            current = data["Close"].iloc[-1]

            if len(data) >= 2:
                previous = data["Close"].iloc[-2]
                change = current - previous
                change_percent = (change / previous) * 100
            else:
                change = 0
                change_percent = 0

            results[name] = {
                "status": "OK",
                "value": round(float(current), 2),
                "change": round(float(change), 2),
                "change_percent": round(float(change_percent), 2),
            }

        except Exception as e:
            results[name] = {
                "status": "Error",
                "error": str(e)
            }

    return results


if __name__ == "__main__":
    market = get_market_data()

    print("\n========== MARKET SNAPSHOT ==========\n")

    for name, data in market.items():
        print(name)

        if data["status"] == "OK":
            print(f"  Value: {data['value']}")
            print(f"  Change: {data['change']}")
            print(f"  Change %: {data['change_percent']}%")
        else:
            print(f"  Status: {data['status']}")

        print()