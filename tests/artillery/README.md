# Load tests using Artillery
[Artillery](https://artillery.io) is an NPM package for doing load testing.

#### Forewarning

Running these kind of tests fire up actual web requests against the servers behind the target domain. **Please** never run them against our production servers—or any of our servers, for that matter—unless absolutely necessary.

## Installation
Assuming you've got NPM installed

``npm install -g artillery``

## Usage

From the root folder

``artillery run [DIR TO YML CONFIG FILE]``
