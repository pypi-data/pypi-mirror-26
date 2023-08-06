# Bears

Bears is a fast and simple alternative to Pandas.

## Goals
- Fast indexing

## API

### Create DataFrame
```py
# with dict
DataFrame(data={'col1':arr1, 'col2':arr2})

# with keys/values
DataFrame(keys=['col1','col2'],values=[arr1,arr2])
```

### Indexing

The recommended way for performance is to get records without column names.
You can index a specific column with df.<column_name>.

```py
df[5]     # [arr1[5], arr2[5]]
df[[1,3]] # DataFrame(data={'col1':arr1[[1,3]], 'col2':arr2[[1,3]]})
df[5:6]   # DataFrame(data={'col1':arr1[5:6], 'col2':arr2[5:6]})
scalar = df[5][df.col1]

df.rows_value()      # [arr1, arr2]
df.rows_value([1,2]) # [arr1[1,2], arr2[1,2]]

df.rows_dict()       # [ {'col1': arr1[0], 'col2': arr2[0]}, {'col1': arr1[1], 'col2': arr2[1]} ]
df.rows_dict([1])    # [ {'col1': arr1[1], 'col2': arr2[1]} ]

df.to_dict()        # {'col1': arr1, 'col2': arr2}
df.to_dict([1,3,5]) # {'col1': arr1[1,3,5], 'col2': arr2[1,3,5]}
```
