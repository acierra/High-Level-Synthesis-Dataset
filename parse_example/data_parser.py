import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.fpgadeveloper.com/list-of-fpga-dev-boards-by-vendor/"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; HW4Parser/1.0)"}

def main():
    r = requests.get(URL, headers=HEADERS, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")

    all_tables = soup.find_all("table")

    dfs = []
    for tbl in all_tables:
        headers = [th.get_text(strip=True) for th in tbl.find_all("th")]
        rows = []
        for tr in tbl.find_all("tr"):
            cells = [td.get_text(strip=True) for td in tr.find_all("td")]
            if cells:
                rows.append(cells)
        if headers and rows:
            dfs.append(pd.DataFrame(rows, columns=headers))

    if dfs:
        df = pd.concat(dfs, ignore_index=True)
        print(df.head(10))
    else:
        print("⚠️ Таблицы не найдены")

if __name__ == "__main__":
    main()
