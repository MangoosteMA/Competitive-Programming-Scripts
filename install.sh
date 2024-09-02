#!/bin/bash

set -e

cp settings.json cpscripts/.
pip3 install .
rm cpscripts/settings.json
