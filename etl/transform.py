import numpy as np
import pandas as pd

UTIL_COLS = [
    "BRAM_Utilization_percentage",
    "DSP_Utilization_percentage",
    "FF_Utilization_percentage",
    "LUT_Utilization_percentage",
]

def transform(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for c in UTIL_COLS:
        if c in out.columns:
            out.loc[out[c] < 0, c] = 0
            out.loc[out[c] > 100, c] = 100
    if "Speedup" in out.columns:
        out.loc[out["Speedup"] < 0, "Speedup"] = np.nan
    return out

