# ElasticSearch extension for the Chaos Toolkit

Chaostoolkit-elasticsearch module provide elasticsearch reporting and status query capability to Chaostoolkit.
It creates an ElasticSearch document defined by the entity. It records the start date time, adds the executed experiment 
to this document and records the end date time. You need an ElasticSearch service to use this extension.
The ElasticSearch service needs to have an index defined by the entity with the name _chaos_.

## Install

The extension is not yet pushed to PyPi. If you would like to use the extension please
checkout the source code and compile it locally. 


### Install python dependencies
First navigate to the project root and run the following command:
```bash
python3 -m pip install -r requirements.txt
```

If you use pipenv and virtual python environment please use the following command:
```bash
pipenv install -r requirements.txt
```

### Install python dev dependencies
```bash
python3 -m pip install -r requirements-dev.txt
```

```bash
pipenv install -r requirements-dev.txt
```

### Build extension locally

```bash
python3 setup.py bdist_wheel;
python3 -m pip install dist/chaostoolkit_elasticsearch-0.0.1-py3-none-any.whl
```

## Usage

To enable the control you need to set the following (experiment or settings file):
```json
{
  "controls": {
    "reporting": {
      "provider": {
        "type": "python",
        "module": "chaoselasticsearch.controls.es",
        "arguments": {
        "host": "localhost",
        "port": 9200,
        "index": "chaos"
        }
      }
    }
  }
}
```
If you want to use the probe please set the following (experiment or variables file):
```json
{
  "configuration": {
    "elasticsearch": {
      "host": "localhost",
      "port": 9200,
      "index": "chaos"
    }
  }
}
```
## Test

To run the extension unit tests: 

```bash
pytest ./tests
```


## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/