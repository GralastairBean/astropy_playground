import numpy as np
import astropy.units as u
from astropy.coordinates import Distance

print("=========================================")
print("DISTANCE MODULUS PLAYGROUND")
print("=========================================")

# Example 1: Calculate Distance Modulus from a known Gaia Distance
# Suppose a Gaia star sits exactly at the edge of your thesis sample (500 pc)
target_distance = 500 * u.pc

# Convert distance directly to a Distance object
dist_obj = Distance(target_distance)

# Extract the distance modulus (m - M)
μ = dist_obj.distmod.value

print(f"For a star at distance: {target_distance}")
print(f" -> The Distance Modulus (m - M) is: {μ:.2f} magnitudes\n")


# Example 2: Calculate Apparent Magnitude (m) of a Solar Twin at 500 pc
# The Sun has an absolute magnitude (M) of roughly 4.83 in the visible band
M_sun = 4.83

# Rearranging the formula: m = M + (m - M)
m_apparent = M_sun + μ

print("If we place a star exactly like our Sun at 500 pc:")
print(f" -> Intrinsic Absolute Magnitude (M): {M_sun}")
print(f" -> Observed Apparent Magnitude (m):  {m_apparent:.2f}")
print("   (Note: Human eyes can see down to magnitude 6. This star needs a telescope.)\n")


# Example 3: Back-calculating Physical Distance from Magnitudes
# Imagine you find a variable star in your sample with:
m_star = 12.5  # how bright it looks
M_star = 2.1   # how bright it actually is

# Calculate the distance modulus value
modulus_value = m_star - M_star

# Invert the formula mathematically: d = 10^((m - M + 5) / 5)
calculated_distance = 10 ** ((modulus_value + 5) / 5)

print("Back-calculating distance from magnitudes:")
print(f" -> Apparent Magnitude (m): {m_star}")
print(f" -> Absolute Magnitude (M): {M_star}")
print(f" -> Calculated Distance:    {calculated_distance:.2f} pc")
print("=========================================")
