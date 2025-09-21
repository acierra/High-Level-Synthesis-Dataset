import pandas as pd

DATA_URL = "https://huggingface.co/datasets/aferikoglou/GNWSIS/resolve/main/GN%CE%A9SIS.csv"

def main():
    raw_data = pd.read_csv(DATA_URL, encoding="utf-8", sep=",")
    print(raw_data.head(10).to_string(index=False))  

if __name__ == "__main__":
    main()