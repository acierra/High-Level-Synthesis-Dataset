#!/usr/bin/env python3

import pandas as pd

DATA_URL = "https://huggingface.co/datasets/aferikoglou/GNWSIS/resolve/main/GN%CE%A9SIS.csv"

def main():
    df = pd.read_csv(DATA_URL, encoding="utf-8", sep=",")
    print(df.head(10).to_string(index=False))

if __name__ == "__main__":
    main()

