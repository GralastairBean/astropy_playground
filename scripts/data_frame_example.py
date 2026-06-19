import numpy as np
import pandas as pd

# Prints a 10-line empty gap at the start of your terminal run
print("\n" * 10)
print("===================================================")
print("LARGE SCALE GALACTIC DATAFRAME CLEANING AND CUTTING")
print("===================================================")

# Set a random seed so the "random" stars are identical every time you run it
# np.random.seed(42)
num_stars = 10000

# 1. Generate realistic mock Gaia data for 10,000 stars
mock_data = {
    # Unique 64-bit style IDs
    "source_id": np.arange(1000000, 1000000 + num_stars),
    
    # Parallaxes ranging randomly from 0.5 to 50.0 milliarcseconds
    "parallax": np.random.uniform(0.5, 50.0, num_stars),
    
    # Astro quality cuts (RUWE). Most are good (~1.0), a few are bad (>1.4)
    "ruwe": np.random.exponential(scale=0.2, size=num_stars) + 0.9,
    
    # Mock Rotational Velocities (V) centered around the disk speed (~0 km/s)
    # But with a tail of slower stars representing the Hercules stream (-50 km/s)
    "v_velocity": np.random.normal(loc=-10.0, scale=15.0, size=num_stars)
}

# 2. Pack everything into our main DataFrame variable: df
df = pd.DataFrame(mock_data)

print(f"Successfully generated 'df' containing {len(df)} stars.")
print("\nFirst 5 rows of the raw dataset:")
print(df.head(100))
print("-----------------------------------------\n")


print("ANALYSIS STEP 1: Calculate Physical Distances")
# Distance (pc) = 1000 / parallax (mas)
df["distance_pc"] = 1000.0 / df["parallax"]
print("\nDistances calculated and appended to df.")
print(df.head(100))
print("-----------------------------------------\n")


print("\nANALYSIS STEP 2: Apply Thesis Quality Cuts")
# Rule: Must be within 500 pc AND have a reliable astrometric fit (ruwe < 1.4)
quality_filter = (df["distance_pc"] <= 500.0) & (df["ruwe"] < 1.4)
clean_df = df[quality_filter]

print(f" -> Original stars: {len(df)}")
print(f" -> Stars matching cuts: {len(clean_df)}")
print(f" -> Eliminated stars: {len(df) - len(clean_df)}")


print("\nANALYSIS STEP 3: Isolate Potential Hercules Members")
# Rule: From our clean pool, find stars lagging in rotation (-55 <= V <= -30 km/s)
hercules_filter = (clean_df["v_velocity"] >= -55.0) & (clean_df["v_velocity"] <= -30.0)
hercules_df = clean_df[hercules_filter]

print(f" -> Found {len(hercules_df)} potential Hercules candidates within 500 pc.")
print("\nSample rows of your final Hercules dataset:")
print(hercules_df.head(100))
print("=========================================")
