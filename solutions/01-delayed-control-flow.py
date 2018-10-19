results = []
for x in data:
    if is_even(x):  # even
        y = dask.delayed(double)(x)
    else:          # odd
        y = dask.delayed(inc)(x)
    results.append(y)

total = dask.delayed(sum)(results)
