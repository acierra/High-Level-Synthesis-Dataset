from pathlib import Path
import shutil
import pandas as pd
from .validate import ensure_required_columns

REQUIRED = [
    "Application_Name", "Device", "Clock_Period_nsec",
    "LUTs", "FFs", "DSPs", "BRAMs",
    "Latency_msec", "Speedup",
    "BRAM_Utilization_percentage",
    "DSP_Utilization_percentage",
    "FF_Utilization_percentage",
    "LUT_Utilization_percentage"
]

def extract(csv_path: str, raw_dir: str) -> pd.DataFrame:
    src = Path(csv_path).expanduser().resolve()
    if not src.exists():
        raise FileNotFoundError(f"CSV not found: {src}")
    raw_dir_p = Path(raw_dir).expanduser().resolve()
    raw_dir_p.mkdir(parents=True, exist_ok=True)
    dst = raw_dir_p / src.name
    if str(src) != str(dst):
        shutil.copyfile(src, dst)
    df = pd.read_csv(src)
    ensure_required_columns(df, REQUIRED)
    return df

