
### Description
This script recursive finds duplicate files below a given directory path. Different 
to most duplication cleanup software, the comparison does not rely on hashing the file
contents, but relies only on matching the filename and matching the size to a 
adjustable  quality factor. The latter, for instance, is set to 98%, that
the file sizes are allowed to differ. Since this comparison is highly ambiguous and error-prone, duplicates are not 
deleted unless confirmed for each case.


### Usage
* see options and parameters
    ```bash
    clean_duplicate_files -h
    ```


##### in development
```bash
python -m duplicate_files <folder>
```


