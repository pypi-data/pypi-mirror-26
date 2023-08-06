# Wheat ![CI status](https://img.shields.io/badge/build-passing-brightgreen.svg)

Wheat is a Python library for generating python project.

## Installation

### Requirements
* Python 2.7 and up

`$ pip install wheat`

## Usage

```bash
wheat

> Enter your project name:
> Enter your name:
> Enter the output dir:

> 1 - mock-logger: Handler for testing logging[Recommended]
> 2 - config: Reading configs from yaml files[Recommended]
> 3 - paddy: Transaction Middlewares
> 4 - orm: Orm for database connection
> Choose packages extended:

> Check for requirements of generated project
> chance-mock-logger ... [False]

> Packages to be installed
> - chance-mock-logger == 1.0.0
> Proceed? [Y/N]

> Creating Directories
> Generating Files
> Initialization Finished
> Running checks
> Successfully create PROJECT at ...
```

## Development
```
$ virtualenv wheat
$ . wheat/bin/activate
$ pip install -e .
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
