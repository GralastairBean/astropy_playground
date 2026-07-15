from pathlib import Path
from datetime import datetime
from time import perf_counter

import pandas as pd
from astroquery.gaia import Gaia


# Proof-of-concept pull settings. Keep this intentionally small so the
# end-to-end pipeline can be validated quickly before expanding the sample.
PARALLAX_MIN_MAS = 5.0
ROW_LIMIT = 5000

QUERY = """
    SELECT TOP {row_limit}
        source_id,
        ra,
        dec,
        parallax,
        pmra,
        pmdec,
        radial_velocity,
        ruwe,
        phot_g_mean_mag,
        phot_bp_mean_mag,
        phot_rp_mean_mag
    FROM gaiadr3.gaia_source
    WHERE parallax IS NOT NULL
        AND parallax > 0
        AND pmra IS NOT NULL
        AND pmdec IS NOT NULL
        AND radial_velocity IS NOT NULL
        AND phot_g_mean_mag IS NOT NULL
        AND phot_bp_mean_mag IS NOT NULL
        AND phot_rp_mean_mag IS NOT NULL
        AND parallax >= {parallax_min_mas}
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

    raw_csv = data_dir / "gaia_real_h1_h2_raw.csv"

    log("Starting proof-of-concept Gaia Hercules data pull.", started_at)
    log(
        (
            "Submitting Gaia DR3 proof-of-concept query for "
            f"up to {ROW_LIMIT:,} sources with parallax >= {PARALLAX_MIN_MAS:.3f} mas..."
        ),
        started_at,
    )
    query = QUERY.format(parallax_min_mas=PARALLAX_MIN_MAS, row_limit=ROW_LIMIT)
    job = Gaia.launch_job_async(query=query)

    log("Gaia query returned. Loading results into pandas...", started_at)
    table = job.get_results()
    df = table.to_pandas()
    log(f"Loaded {len(df):,} rows.", started_at)

    log(f"Saving raw query results to {raw_csv}...", started_at)
    df.to_csv(raw_csv, index=False)

    log("Finished proof-of-concept Gaia Hercules data pull.", started_at)


if __name__ == "__main__":
    main()