# matly
matplotlib syntax for plotly

## Requirements
There are several fiddly packages that are required for plotly and these don't have consistency in the
package managing tool that can install them. For that reason it is advised that you have homebrew installed
as well as conda or npm

## Add path
To add the locations of the files to your path so that python can find all the code run
```
source .matly_env
```

# Importing requirements
## Pip
Some python package dependencies can't be installed using pip.

To install the packages that can be install through pip use
```
make requirements
```

## Homebrew
If you don't already have homebrew installed then type the following command into the terminal:
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Note that the terminal window will ask for your mac password and then will present 2 commands that you need to paste into the terminal.

## npm
You might need npm in the orca installation (below). If you go down that route then use the command:
```
brew install node
```

## ORCA
Then you'll need to install plotly-orca. There are three options here: https://plotly.com/python/orca-management/

## Poppler
You'll also need poppler which is not available through pip and must be installed using homebrew.
```
brew install poppler
```

# Testing
To run unit tests run the following commands:
- Set up the virtual environment: `make create_environment`
- Activate virtual environment: `. venv/bin/activate`
- Add path to `src` folder: `source .matly_env`
- Run tests: `make test`

To clean up after running tests run the following commands:
- Deactivate virtual environment: `deactivate`
- Remove virtual environment: `make clean`
- Clean up `PATH` and `PYTHONPATH`: `source .clean_matly_env`
