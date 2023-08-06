# p-tree 0.1.14

## About
```
This package is used to count the CFUs in petri dishes.
In order to use it you must provide it with a shared dropbox link to a directory containing the images in a png format.
Only images must be contained in the directory no subdirectories.
```


### Installation
```
This package requires python==3.6

to install type:

pip install p-tree

or

pip install --upgrade p-tree
```


### Example Script


```python
from p_tree.run import CountColonies

if __name__ == '__main__':
    url = 'https://www.dropbox.com/sh/vq4wb9fd9k1fz49/AADLR3IIgj8lMWs8m9QLzdPoa?dl=1'
    cc = CountColonies(url=url)
    dfs = cc.main()
    print(dfs)
```

# TODO

1. Provide rotate angle option and number of rotations.
2. Accept directory as input and not only dropbox shared link.
3. Save DataFrames to csv.
4. Output analytics such as bell curves (mean and std) for all petries.


