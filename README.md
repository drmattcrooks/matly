# mattsplotlib
matplotlib syntax for plotly

## Requirements
There are several fiddly packages that are required for plotly and these don't have consistency in the
package managing tool that can install them. For that reason it is advised that you have homebrew installed
as well as conda or npm

## Add path
To add the locations of the files to your path so that python can find all the code run
```
source .mattsplotlib_env
```

# Importing requirements
## Pip
Some python package dependencies can't be installed using pip.

To install the packages that can be install through pip use
```
make requirements
```

## ORCA
Then you'll need to install plotly-orca. There are three options here: https://plotly.com/python/orca-management/

## Poppler
You'll also need poppler which is not available through pip and must be installed using homebrew.
```
brew install poppler
```
