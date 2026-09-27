import yfinance as yf

SYMBOLS = {
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "Dow Jones": "^DJI",
    "Nikkei 225": "^N225",
    "Hang Seng": "^HSI",
    "Crude Oil": "CL=F",
    "Gold": "GC=F",
    "USD/INR": "INR=X",
}


def get_global_data():
    results = {}

    for name, symbol in SYMBOLS.items():
        try:
            data = yf.Ticker(symbol).history(period="5d")

            if data.empty:
                results[name] = {"status": "No data"}
                continue

            current = float(data["Close"].iloc[-1])

            if len(data) >= 2:
                previous = float(data["Close"].iloc[-2])
                change = current - previous
                change_percent = (change / previous) * 100
            else:
                change = 0
                change_percent = 0

            results[name] = {
                "status": "OK",
                "value": round(current, 2),
                "change": round(change, 2),
                "change_percent": round(change_percent, 2),
            }

        except Exception as error:
            results[name] = {
                "status": "Error",
                "error": str(error)
            }

    return results


if __name__ == "__main__":
    global_data = get_global_data()

    print("\n========== GLOBAL MARKET DATA ==========\n")

    for name, data in global_data.items():
        print(name)

        if data["status"] == "OK":
            print(f"  Value: {data['value']}")
            print(f"  Change: {data['change']}")
            print(f"  Change %: {data['change_percent']}%")
        else:
            print(f"  Status: {data['status']}")

        print()