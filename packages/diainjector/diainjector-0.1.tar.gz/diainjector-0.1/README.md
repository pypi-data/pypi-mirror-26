# Diainjector

## Synopsis

This is a simple dependency injector implementation used in dia-backend project.

## Code Example

`from diainjector import injector`

`implementation = injector.request_implementation(AbstractClassInterface)`

And from other module or package:

`from diainjector import injector`

`implementation = AbstractClassInterfaceImplemented()`

`injector.provide_implementation(AbstractClassInterface, implementation)`


## Motivation

The core of dia-backend is a framework that runs above a Django project but it doesn't know that runs above Django. To help us to get this working we needed this simple dependency injector.

## Installation

`git clone https://github.com/koyadovic/diainjector.git`

`pip install diainjector`

## Tests

There is no tests for now yet.

## Contributors

m.collado.gomez at gmail dot com

## License

GPL 2.0