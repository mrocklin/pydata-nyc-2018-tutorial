results = []

for x in data:
    y = dask.delayed(inc)(x)
    results.append(y)

total = dask.delayed(sum)(results)
print("Before computing:", total)  # Let's see what type of thing total is
result = total.compute()
print("After computing :", result)  # After it's computed
