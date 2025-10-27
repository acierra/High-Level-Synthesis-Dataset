import argparse
import pandas as pd
import sqlite3
from pathlib import Path
from sqlalchemy import create_engine

def load_csv(path: str | None) -> pd.DataFrame:
    default = Path("notebook/newdata/gnwsis_clean.csv")
    p = Path(path) if path else default
    if not p.exists():
        raise FileNotFoundError(f"Не найден CSV {p}")
    return pd.read_csv(p)

def load_creds(creds_path: str) -> dict:
    if not Path(creds_path).exists():
        raise FileNotFoundError(f"Не найден файл {creds_path}")
    conn = sqlite3.connect(creds_path)
    try:
        row = pd.read_sql("SELECT * FROM access LIMIT 1", conn).iloc[0].to_dict()
    finally:
        conn.close()
    return row

def make_engine(creds: dict, db_name: str | None):
    db = db_name or creds.get("db") or "homeworks"
    url = creds["url"]
    port = creds["port"]
    user = creds["user"]
    pwd = creds["pass"]
    return create_engine(f"postgresql+psycopg2://{user}:{pwd}@{url}:{port}/{db}")

def write_to_db(df: pd.DataFrame, table: str, engine):
    df_head = df.head(100)
    with engine.begin() as conn:
        df_head.to_sql(table, con=conn, schema="public", if_exists="replace", index=False, method="multi", chunksize=1000)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--table", required=True)
    parser.add_argument("--csv", required=False)
    parser.add_argument("--creds", default="creds.db")
    parser.add_argument("--db", required=False)
    args = parser.parse_args()

    df = load_csv(args.csv)
    print(f"Загружен файл: {Path(args.csv) if args.csv else Path('notebook/newdata/gnwsis_clean.csv')}, форма: {df.shape}")

    creds = load_creds(args.creds)
    print(f"Учётные данные: {{'url': '{creds['url']}', 'port': '{creds['port']}', 'user': '{creds['user']}', 'pass': '{creds['pass']}'}}")

    engine = make_engine(creds, args.db)
    write_to_db(df, args.table, engine)

if __name__ == "__main__":
    main()
