from pathlib import Path
import sqlite3
import pandas as pd
from sqlalchemy import create_engine

def read_creds(creds_db: str) -> dict:
    p = Path(creds_db).expanduser().resolve()
    with sqlite3.connect(p) as conn:
        row = pd.read_sql("SELECT * FROM access LIMIT 1", conn).iloc[0].to_dict()
    return row

def to_parquet(df: pd.DataFrame, out_dir: str, name="dataset.parquet") -> str:
    out_p = Path(out_dir).expanduser().resolve()
    out_p.mkdir(parents=True, exist_ok=True)
    path = out_p / name
    df.to_parquet(path, index=False)
    return str(path)

def to_postgres(df: pd.DataFrame, table: str, creds: dict, limit: int = 100):
    url = creds["url"]
    port = creds["port"]
    user = creds["user"]
    pwd = creds["pass"]
    engine = create_engine(f"postgresql+psycopg2://{user}:{pwd}@{url}:{port}/homeworks")
    df.head(limit).to_sql(table, engine, if_exists="replace", index=False)

