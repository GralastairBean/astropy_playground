import astropy.units as u
from astropy.coordinates import Distance

print("=========================================")
print("GAIA PARALLAX TO DISTANCE CONVERSION")
print("=========================================")

# Simulate raw parallax values in milliarcseconds (mas) from Gaia
# Star 1 has a large parallax (closer), Star 2 has a tiny parallax (further)
parallax_star1 = 25.4 * u.mas
parallax_star2 = 2.1 * u.mas

# Convert parallax directly to distance objects
dist1 = Distance(parallax=parallax_star1)
dist2 = Distance(parallax=parallax_star2)

# Extract distances in parsecs (pc) and light-years (ly)
print(f"Star 1 Distance: {dist1.pc:.2f} pc ({dist1.lyr:.2f} light-years)")
print(f"Star 2 Distance: {dist2.pc:.2f} pc ({dist2.lyr:.2f} light-years)")
print("=========================================")
