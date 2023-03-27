# matly
matplotlib syntax for plotly

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
