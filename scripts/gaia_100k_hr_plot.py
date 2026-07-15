from pathlib import Path
from datetime import datetime
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def log(message: str, started_at: float) -> None:
    elapsed_seconds = perf_counter() - started_at
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp} | +{elapsed_seconds:7.2f}s] {message}", flush=True)


def main() -> None:
    started_at = perf_counter()
    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data"
    input_csv = data_dir / "gaia_100000_closest_stars.csv"
    output_plot_png = data_dir / "gaia_100000_hr_diagram.png"
    output_plot_pdf = data_dir / "gaia_100000_hr_diagram.pdf"

    log(f"Loading Gaia data from {input_csv}...", started_at)
    df = pd.read_csv(input_csv)
    log(f"Loaded {len(df):,} rows.", started_at)

    log("Computing HR-diagram columns.", started_at)
    hr_df = df.copy()
    hr_df["bp_rp"] = hr_df["phot_bp_mean_mag"] - hr_df["phot_rp_mean_mag"]
    hr_df["abs_g"] = hr_df["phot_g_mean_mag"] + 5 * np.log10(hr_df["parallax"]) - 10
    hr_df = hr_df.replace([np.inf, -np.inf], np.nan).dropna(subset=["bp_rp", "abs_g"])
    log(f"HR diagram data ready with {len(hr_df):,} rows.", started_at)

    log("Creating HR diagram plot.", started_at)
    fig, ax = plt.subplots(figsize=(8, 9))
    ax.scatter(
        hr_df["bp_rp"],
        hr_df["abs_g"],
        s=3,
        c="black",
        alpha=0.35,
        edgecolors="none",
    )

    ax.set_xlabel("BP - RP")
    ax.set_ylabel("Absolute G magnitude")
    ax.set_title("Gaia 100,000 Closest Stars HR Diagram")
    ax.invert_yaxis()
    ax.grid(True, linestyle="--", alpha=0.3)

    plt.tight_layout()
    log(f"Saving HR diagram PNG to {output_plot_png}...", started_at)
    plt.savefig(output_plot_png, dpi=300)
    log(f"Saving HR diagram PDF to {output_plot_pdf}...", started_at)
    plt.savefig(output_plot_pdf)
    plt.show()

    log(f"Saved HR diagram to: {output_plot_png}", started_at)
    log(f"Saved HR diagram to: {output_plot_pdf}", started_at)


if __name__ == "__main__":
    main()
