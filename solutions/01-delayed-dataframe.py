# copied sequential code
sums = []
counts = []

def filename_to_dataframe(fn):
    gcs = gcsfs.GCSFileSystem()

    with gcs.open(fn) as f:
        pf = pq.ParquetFile(f)  # Arrow ParquetFile
        table = pf.read()       # Arrow Table
        df = table.to_pandas()  # Pandas DataFrame

    return df


for fn in filenames:

    # Read in parquet file to Pandas Dataframe
    df = dask.delayed(filename_to_dataframe)(fn)

    # Groupby origin airport
    total = df.passenger_count.sum()

    # Number of flights by origin
    count = df.passenger_count.count()

    # Save the intermediates
    sums.append(total)
    counts.append(count)

# Combine intermediates to get total mean-delay-per-origin
total_sums = dask.delayed(sum)(sums)
total_counts = dask.delayed(sum)(counts)
mean = total_sums / total_counts
mean
