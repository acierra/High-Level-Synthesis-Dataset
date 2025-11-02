import sys
import importlib
import argparse

REQUIRED = [
    ("pandas", "pandas"),
    ("numpy", "numpy"),
    ("sqlalchemy", "sqlalchemy"),
    ("psycopg2", "psycopg2-binary")
]

OPTIONAL = [("pyarrow", "pyarrow")]

def check_deps():
    missing = []
    for mod, pkg in REQUIRED:
        try:
            importlib.import_module(mod)
        except ImportError:
            missing.append(pkg)
    if missing:
        cmd = "pip install " + " ".join(missing)
        print("Не найдены зависимости:", ", ".join(missing))
        print("Установите:", cmd)
        sys.exit(1)

def has_optional():
    avail = {}
    for mod, pkg in OPTIONAL:
        try:
            importlib.import_module(mod)
            avail[mod] = True
        except ImportError:
            avail[mod] = False
    return avail

def main():
    check_deps()
    opt = has_optional()
    from etl.extract import extract
    from etl.transform import transform
    from etl.validate import validate_ranges, head_nonempty
    from etl.load import read_creds, to_parquet, to_csv, to_postgres

    p = argparse.ArgumentParser()
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
    if opt.get("pyarrow", False):
        to_parquet(df, args.outdir, "gnwsis.parquet")
    else:
        to_csv(df, args.outdir, "gnwsis.csv")
    creds = read_creds(args.creds)
    to_postgres(df, args.table, creds, args.limit)
    print("ETL завершён")

if __name__ == "__main__":
    main()
