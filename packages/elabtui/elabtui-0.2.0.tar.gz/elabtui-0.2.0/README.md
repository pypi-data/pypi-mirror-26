# elabtui

## Description

`elabtui` is a text user interface to [elabftw](https://github.com/elabftw/elabftw). It is a python script that uses the REST API.

This project is more a proof-of-concept than anything, but if you want to try, it should work as expected.

## Installation

~~~bash
sudo pip install elabtui
~~~

## Configuration

~~~bash
mkdir ~/.config/elabtui
$EDITOR ~/.config/elabtui/config.yml
~~~

The `config.yml` file should look like this:

~~~yaml
token: 9c7f84d3308c217f65db5541a1e15785d8dfbc2488a69dc30e2e8bae97d0099054c8e6ac91ec1559b468
endpoint: https://elabftw.example.org/api/v1/
~~~

## Usage

~~~bash
elabtui
~~~

## Make new release

* edit `setup.py` and `elabtui/__init__.py` to change version
* python setup.py sdist bdist_egg bdist_wheel
* twine upload dist/*
