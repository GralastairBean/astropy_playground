import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Print empty gap at the start of terminal for clean run
print("\n" * 5)
print("===================================================")
print("LARGE SCALE GALACTIC DATAFRAME CLEANING AND CUTTING")
print("===================================================")

# To Force terminal to display all rows without hiding anything uncomment below line...
# pd.set_option("display.max_rows", None)

# set number of starts for the simulation
num_stars = 50000

# 1. Generate realistic mock Gaia data
print("ANALYSIS STEP 1: Generate realistic mock Gaia data")
mock_data = {
    "source_id": np.arange(1000000, 1000000 + num_stars),
    "parallax": np.random.uniform(0.5, 50.0, num_stars),
    "ruwe": np.random.exponential(scale=0.2, size=num_stars) + 0.9,
    "v_velocity": np.random.normal(loc=-25.0, scale=15.0, size=num_stars),
    "z_height": np.random.normal(loc=0.0, scale=150.0, size=num_stars)
}
print(f"Generated mock Gaia data for {num_stars} stars")
print("-----------------------------------------\n")


# 2. Pack everything into the main DataFrame variable: df
print("ANALYSIS STEP 2: Generate main DataFrame variable")
df = pd.DataFrame(mock_data)

print(f"Successfully generated 'df' containing {len(df)} stars.")
print(df.head(100)) #arbitrarily large number tyo force terminal to show first and last 5 rows
print("-----------------------------------------\n")


# 3. Calculate Physical Distances and add to df
print("ANALYSIS STEP 3: Calculate Physical Distances")
# Distance (pc) = 1000 / parallax (mas)
df["distance_pc"] = 1000.0 / df["parallax"]
print("\nDistances calculated and appended to df.")
print(df.head(100))
print("-----------------------------------------\n")


# 4. Apply Filter Quality Cuts, Rule: Must be within 500 pc AND have a reliable astrometric fit (ruwe < 1.4)
print("\nANALYSIS STEP 4: Apply Filter Quality Cuts: <500 pc AND have reliable astrometric fit (ruwe < 1.4)")
quality_filter = (df["distance_pc"] <= 500.0) & (df["ruwe"] < 1.4)
clean_df = df[quality_filter].copy() # Using .copy() avoids a common pandas warning

print(f" -> Original stars: {len(df)}")
print(f" -> Eliminated stars: {len(df) - len(clean_df)}")
print(f" -> Stars matching cuts: {len(clean_df)}")


# 5. Split into Hercules 1 and Hercules 2 Substructures based on velocity boundaries
print("\nANALYSIS STEP 5: Split into Hercules 1 and Hercules 2 Substructures based on velocity boundaries")
# Following your thesis protocol, we split the Hercules stream based on velocity boundaries
h1_filter = (clean_df["v_velocity"] >= -55.0) & (clean_df["v_velocity"] < -43.0)
h2_filter = (clean_df["v_velocity"] >= -43.0) & (clean_df["v_velocity"] <= -30.0)

h1_df = clean_df[h1_filter]
h2_df = clean_df[h2_filter]

print(f" -> Isolated {len(h1_df)} Hercules 1 (H1) members.")
print(f" -> Isolated {len(h2_df)} Hercules 2 (H2) members.")
print(f" -> Removed {len(clean_df) - len(h1_df) - len(h2_df)} non-member stars.")
print("=========================================\n")


# 6. Plotting Results
print("ANALYSIS STEP 4: Advanced Plotting (KDE Curves and CDFs)")

# Initialize a figure with two side-by-side subplots for maximum thesis impact
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# ----------------------------------------------------
# SUBPLOT 1: Smooth Probability Density (KDE Style)
# ----------------------------------------------------
# We use a high number of bins with histtype='step' to create a smooth curve
ax1.hist(h1_df["z_height"], bins=100, range=(-500, 500), density=True, 
         histtype="step", linewidth=2.5, color="darkgreen", label="Hercules 1 (H1)")

ax1.hist(h2_df["z_height"], bins=100, range=(-500, 500), density=True, 
         histtype="step", linewidth=2.5, color="darkorange", label="Hercules 2 (H2)")

# Fill the area underneath slightly so they stand out
ax1.hist(h1_df["z_height"], bins=100, range=(-500, 500), density=True, alpha=0.1, color="darkgreen")
ax1.hist(h2_df["z_height"], bins=100, range=(-500, 500), density=True, alpha=0.1, color="darkorange")

ax1.set_title("Stellar Probability Density Profile", fontsize=12, pad=10)
ax1.set_xlabel("Galactic Height z (parsecs)", fontsize=11)
ax1.set_ylabel("Probability Density", fontsize=11)
ax1.set_xlim(-500, 500)
ax1.grid(True, linestyle="--", alpha=0.5)
ax1.legend(fontsize=10, loc="upper right")

# ----------------------------------------------------
# SUBPLOT 2: Cumulative Distribution Function (CDF)
# ----------------------------------------------------
# Setting cumulative=True turns the histogram into a running total fraction (0 to 1)
ax2.hist(h1_df["z_height"], bins=500, range=(-500, 500), density=True, cumulative=True,
         histtype="step", linewidth=2.5, color="darkgreen", label="H1 Cumulative")

ax2.hist(h2_df["z_height"], bins=500, range=(-500, 500), density=True, cumulative=True,
         histtype="step", linewidth=2.5, color="darkorange", label="H2 Cumulative")

ax2.set_title("Cumulative Spatial Distribution (CDF)", fontsize=12, pad=10)
ax2.set_xlabel("Galactic Height z (parsecs)", fontsize=11)
ax2.set_ylabel("Fraction of Total Population", fontsize=11)
ax2.set_xlim(-500, 500)
ax2.set_ylim(0, 1.05)
ax2.grid(True, linestyle="--", alpha=0.5)
ax2.legend(fontsize=10, loc="lower right")

plt.suptitle("Vertical Structure Comparison: Hercules 1 vs Hercules 2", fontsize=14, y=0.98)
plt.tight_layout()

# Save the advanced multi-panel figure
plt.savefig("scripts/h1_h2_advanced_comparison.png", dpi=300)
print(" -> Advanced figure saved as: scripts/h1_h2_advanced_comparison.png")

plt.show()
print("=========================================")
