#!/bin/sh -l

echo "Coronavirus Data Collection"
time=$(date)
echo "::set-output name=time::$time"

python3 -m venv env;
source env/bin/activate;
pip install -r requirements.txt;
python3 scraper.py;
