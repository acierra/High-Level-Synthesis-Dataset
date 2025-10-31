import pandas as pd

DATA_URL = "https://huggingface.co/datasets/aferikoglou/GNWSIS/resolve/main/GN%CE%A9SIS.csv"

def main():
    raw_data = pd.read_csv(DATA_URL, encoding="utf-8", sep=",")
    print("=== RAW head(10) ===")
    print(raw_data.head(10))

    df = raw_data.copy()

    float_cols = [
        "Clock_Period_nsec", "Latency_msec", "Synthesis_Time_sec", "Speedup",
        "BRAM_Utilization_percentage", "DSP_Utilization_percentage",
        "FF_Utilization_percentage", "LUT_Utilization_percentage"
    ]
    for c in float_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(
                df[c].astype(str).str.replace(",", ".", regex=False),
                errors="coerce"
            ).astype("float64")

    int_cols = ["BRAMs", "DSPs", "FFs", "LUTs"]
    for c in int_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")

    cat_cols = ["Application_Name", "Version", "Device"]
    for c in cat_cols:
        if c in df.columns:
            df[c] = df[c].astype("category")

    dir_cols = [c for c in df.columns if c.startswith(("Array_", "OuterLoop_", "InnerLoop_"))]
    for c in dir_cols:
        df[c] = df[c].astype("category")
    print(df.head(10))
    print(df.dtypes)

if __name__ == "__main__":
    main()