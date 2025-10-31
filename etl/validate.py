import pandas as pd

def ensure_required_columns(df: pd.DataFrame, required: list[str]) -> None:
    miss = [c for c in required if c not in df.columns]
    if miss:
        raise ValueError(f"Missing required columns: {miss}")

def validate_ranges(df: pd.DataFrame) -> None:
    cols = [
        "BRAM_Utilization_percentage",
        "DSP_Utilization_percentage",
        "FF_Utilization_percentage",
        "LUT_Utilization_percentage"
    ]
    for c in cols:
        if c in df.columns:
            bad = df[c].dropna().between(0, 100).value_counts().get(False, 0)
            if bad > 0:
                raise ValueError(f"Column {c} has {bad} invalid values")
    if "Speedup" in df.columns:
        bad = (df["Speedup"].dropna() < 0).sum()
        if bad > 0:
            raise ValueError(f"Speedup has {bad} negative values")

def head_nonempty(df: pd.DataFrame):
    if len(df) == 0:
        raise ValueError("Empty dataframe after processing")

