#!/bin/bash

cp settings.json cpscripts/.
pip3 install .
rm cpscripts/settings.json
