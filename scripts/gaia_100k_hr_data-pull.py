from pathlib import Path
from datetime import datetime
from time import perf_counter
from astroquery.gaia import Gaia

# Give me up to 100,000 Gaia DR3 sources that have valid positive parallax 
# and valid G/BP/RP photometry, sorted from nearest to farthest away...
# Note this will take ~ 30 min.
QUERY = """
    SELECT TOP 100000
        source_id,
        ra,
        dec,
        parallax,
        phot_g_mean_mag,
        phot_bp_mean_mag,
        phot_rp_mean_mag
    FROM gaiadr3.gaia_source
    WHERE parallax IS NOT NULL
        AND parallax > 0
        AND phot_g_mean_mag IS NOT NULL
        AND phot_bp_mean_mag IS NOT NULL
        AND phot_rp_mean_mag IS NOT NULL
    ORDER BY parallax DESC
"""


def log(message: str, started_at: float) -> None:
    elapsed_seconds = perf_counter() - started_at
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp} | +{elapsed_seconds:7.2f}s] {message}", flush=True)


def main() -> None:
    started_at = perf_counter()
    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)

    output_csv = data_dir / "gaia_100000_closest_stars.csv"

    log("Starting Gaia 100k-star example.", started_at)
    log("Preparing ADQL query for 100,000 nearby stars.", started_at)
    log("Submitting Gaia query...", started_at)
    job = Gaia.launch_job_async(query=QUERY)

    log("Gaia query returned. Downloading results into memory...", started_at)
    table = job.get_results()
    df = table.to_pandas()
    log(f"Loaded {len(df):,} rows into a pandas DataFrame.", started_at)

    log(f"Saving full table to {output_csv}...", started_at)
    df.to_csv(output_csv, index=False)
    log("CSV save complete.", started_at)

    preview = df.head(10)
    log("Printing first 10 rows only.", started_at)
    print("First 10 rows only:\n")
    print(preview.to_string(index=False))
    print(f"\nSaved full 100,000-row table to: {output_csv}")
    log("Finished all steps.", started_at)


if __name__ == "__main__":
    main()