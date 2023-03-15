# MarketWatch-Scraper
Scrape stock data from MarketWatch for usage in ML programs or anything else.

Usage:
```bash
pip install -r requirements.txt
py scrape.py --stock STOCK [--timeout TIMEOUT]
```

Example:
```bash
py scrape.py --stock AAPL
py scrape.py --stock GME [--timeout 3]
```
