import argparse
from .extract import extract
from .transform import transform
from .validate import validate_ranges, head_nonempty
from .load import read_creds, to_parquet, to_postgres

def main():
    p = argparse.ArgumentParser(description="ETL pipeline for HLS dataset")
    p.add_argument("--csv", required=True)
    p.add_argument("--creds", required=True)
    p.add_argument("--table", required=True)
    p.add_argument("--rawdir", default="data/raw")
    p.add_argument("--outdir", default="data/processed")
    p.add_argument("--limit", type=int, default=100)
    args = p.parse_args()

    df = extract(args.csv, args.rawdir)
    df = transform(df)
    validate_ranges(df)
    head_nonempty(df)
    to_parquet(df, args.outdir, "gnwsis.parquet")
    creds = read_creds(args.creds)
    to_postgres(df, args.table, creds, args.limit)
    print("ETL completed successfully")

if __name__ == "__main__":
    main()

