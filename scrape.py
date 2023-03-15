import datetime, requests, csv, argparse

class MarketwatchScraper():
    def __init__(self, stock: str = "AAPL", timeout: int = 1) -> None:
        self.stock = stock
        self.timeout = timeout
        pass

    def scrape(self) -> None:
        self.saveToFile(self.getURLS())

    def saveToFile(self, urls: list) -> None:
        localFile = f"{self.stock.lower()}.csv"
        with open(localFile, "w") as f:
            f.write("Date,Open,High,Low,Close,Volume\n")
            f.close()
        for url in urls:
            print(f"Getting data from url {url}...")

            try:
                resp = requests.get(url, timeout=self.timeout, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 OPR/96.0.0.0 (Edition std-1)"
                })
                if resp.status_code != 200:
                    print(f"Error! Status code: {resp.status_code}")
                    continue
            except Exception as e:
                print(f"Error! Exception: {e}")
                continue

            data = resp.content.decode("utf-8")
            csvData = csv.reader(data.splitlines(), delimiter=",")
            next(csvData)
            with open(localFile, "a") as f:
                print(f"Writing data to {localFile}...")
                writer = csv.writer(f)
                for row in csvData:
                    writer.writerow(row)
                f.close()

    def getURLS(self) -> list:
        urls = []
        startDate = datetime.datetime(1970, 1, 1)
        endDate = datetime.datetime.today()
        if endDate > datetime.datetime.today():
            endDate = datetime.datetime.today()

        while startDate < endDate:
            date1 = startDate.strftime("%m/%d/%Y%%2000:00:00")
            date2 = (startDate + datetime.timedelta(days=366)).strftime("%m/%d/%Y%%2000:00:00")
            url = f"https://www.marketwatch.com/investing/stock/{self.stock}/downloaddatapartial?startdate={date1}&enddate={date2}&daterange=d30&frequency=p1d&csvdownload=true&downloadpartial=false&newdates=false"
            print(f"Added URL for {startDate.strftime('%m/%d/%Y')} to {(startDate + datetime.timedelta(days=366)).strftime('%m/%d/%Y')}")
            urls.append(url)
            startDate = startDate + datetime.timedelta(days=365) 
        
        return urls
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stock", type=str, required=True)
    parser.add_argument("--timeout", type=int, required=False)
    args = parser.parse_args()

    scraper = MarketwatchScraper(stock=args.stock, timeout=args.timeout if args.timeout else 1)
    scraper.scrape()