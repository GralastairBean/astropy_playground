import astropy.coordinates as coord
import astropy.units as u

print("=========================================")
print("VELOCITY VECTOR PLAYGROUND")
print("=========================================")

# 1. Input mock 6D data for a local star (similar to a Gaia DR3 row)
star_6d = coord.SkyCoord(
    ra=280.0 * u.deg,
    dec=40.0 * u.deg,
    distance=100.0 * u.pc,
    pm_ra_cosdec=-15.0 * u.mas / u.yr,
    pm_dec=-35.0 * u.mas / u.yr,
    radial_velocity=-40.0 * u.km / u.s,
    frame="icrs",
)

# 2. Transform the star into the Galactocentric Frame
# This automatically calculates U, V, and W space velocities
galactocentric = star_6d.transform_to(coord.Galactocentric)

# 3. Extract U and V components (v_x is U, v_y is V, z is vertical position)
U_velocity = galactocentric.v_x.value
V_velocity = galactocentric.v_y.value
Z_height = galactocentric.z.value

print("Calculated Physical Properties:")
print(f" -> Vertical Height (Z):    {Z_height:.2f} pc")
print(f" -> Radial Velocity (U):    {U_velocity:.2f} km/s")
print(f" -> Rotational Velocity (V): {V_velocity:.2f} km/s\n")

# 4. Check if this star matches our Hercules criteria
# Hercules rotates slower than the rest of the disk (V around -30 to -55 km/s)
if -55 <= V_velocity <= -30:
    print("RESULT: This star is a match for the Hercules Moving Group.")
else:
    print("RESULT: This is a normal background disk star.")
print("=========================================")
