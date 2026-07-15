from astroquery.gaia import Gaia

query = """
	SELECT TOP 5
		source_id,
		ra,
		dec,
		phot_g_mean_mag
	FROM gaiadr3.gaia_source
	WHERE phot_g_mean_mag IS NOT NULL
"""

print("Sending Gaia query...", flush=True)
job = Gaia.launch_job(query=query)

print("Gaia query returned, fetching results...", flush=True)
result = job.get_results()

print(result)
