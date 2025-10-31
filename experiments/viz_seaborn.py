import argparse, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_csv(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV не найден: {path}")
    return pd.read_csv(path)

def p99_clip(s):
    hi = np.nanpercentile(s, 99)
    lo = np.nanpercentile(s, 1)
    return s.clip(lo, hi)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="notebook/newdata/gnwsis_clean.csv")
    parser.add_argument("--out", default="docs/plots")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({"figure.figsize":(9,6), "axes.titlesize":14, "axes.labelsize":12})

    df = load_csv(args.csv)

    num_cols = [c for c in [
        "Speedup","Latency_msec","Clock_Period_nsec",
        "LUTs","FFs","DSPs","BRAMs",
        "LUT_Utilization_percentage","FF_Utilization_percentage",
        "DSP_Utilization_percentage","BRAM_Utilization_percentage"
    ] if c in df.columns]

    df_num = df[num_cols].apply(pd.to_numeric, errors="coerce")
    df_clip = df_num.apply(p99_clip)

    g = df_clip[["Clock_Period_nsec","Latency_msec","Speedup"]].hist(bins=50, layout=(1,3))
    plt.tight_layout()
    plt.savefig(os.path.join(args.out, "hist_core_metrics.png"), dpi=160)
    plt.close()

    _, ax = plt.subplots()
    sns.boxplot(x=df_clip["Speedup"], ax=ax)
    ax.set_title("Boxplot: Speedup (обрезка по 99-му перцентилю)")
    ax.set_xlabel("Speedup")
    plt.savefig(os.path.join(args.out, "box_speedup.png"), dpi=160)
    plt.close()

    _, ax = plt.subplots()
    sns.scatterplot(x=df_clip["Latency_msec"], y=df_clip["Speedup"], s=10, ax=ax)
    ax.set_title("Speedup vs Latency")
    ax.set_xlabel("Latency_msec")
    ax.set_ylabel("Speedup")
    plt.savefig(os.path.join(args.out, "scat_speedup_latency.png"), dpi=160)
    plt.close()

    util_cols = [c for c in df_clip.columns if c.endswith("_Utilization_percentage")]
    util_cols = util_cols[:4] if len(util_cols)>4 else util_cols
    if "Speedup" in df_clip and util_cols:
        fig, axs = plt.subplots(2, 2, figsize=(11,8))
        axs = axs.ravel()
        for i,c in enumerate(util_cols):
            sns.scatterplot(x=df_clip[c], y=df_clip["Speedup"], s=10, ax=axs[i])
            axs[i].set_title(f"Speedup vs {c}")
            axs[i].set_xlabel(c); axs[i].set_ylabel("Speedup")
        plt.tight_layout()
        plt.savefig(os.path.join(args.out, "scat_speedup_vs_utils.png"), dpi=160)
        plt.close()

    pair_cols = [c for c in ["Speedup","LUTs","FFs","DSPs","BRAMs"] if c in df_clip.columns]
    if len(pair_cols) >= 3:
        g = sns.pairplot(df_clip[pair_cols].sample(min(3000, len(df_clip)), random_state=args.seed), diag_kind="hist")
        g.fig.suptitle("Pairplot: ресурсы и Speedup", y=1.02)
        g.savefig(os.path.join(args.out, "pairplot_resources_speedup.png"), dpi=160)
        plt.close()

    corr = df_clip.corr(numeric_only=True)
    _, ax = plt.subplots(figsize=(9,7))
    sns.heatmap(corr, cmap="coolwarm", center=0, ax=ax)
    ax.set_title("Корреляции числовых признаков")
    plt.tight_layout()
    plt.savefig(os.path.join(args.out, "corr_heatmap.png"), dpi=160)
    plt.close()

if __name__ == "__main__":
    main()
