# mattsplotlib
matplotlib syntax for plotly

## Requirements
There are several fiddly packages that are required for plotly and these don't have consistency in the
package managing tool that can install them. For that reason it is advised that you have homebrew installed
as well as conda or npm

## Add path
If you're on a newer mac that uses zsh then run this in the command line:
```
echo 'export PATH="{local_path_to_mattsplotlib}/src:$PATH"' >> ~/.zshrc
```

If you're on an older mac that uses bash shell then run this in the command line:
```
echo 'export PATH="{local_path_to_mattsplotlib}/src:$PATH"' >> ~/.bash_profile
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
```
brew install poppler
```