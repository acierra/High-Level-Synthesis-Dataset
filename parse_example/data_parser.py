#!/usr/bin/env python3
import pandas as pd
import requests
from io import StringIO

URL = "https://www.fpgadeveloper.com/list-of-fpga-dev-boards-by-vendor/"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; HW4Parser/1.0)"}

def main():
    r = requests.get(URL, headers=HEADERS, timeout=30)
    r.raise_for_status()
    html = r.text
    tables = pd.read_html(StringIO(html))
    tables = [t for t in tables if not t.empty]
    df = pd.concat(tables, ignore_index=True)
    print(df.head(10))

if __name__ == "__main__":
    main()
