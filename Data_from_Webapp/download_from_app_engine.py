#!/usr/bin/env python

from os import system, listdir, remove

if "raw_data.csv" in listdir:
    remove("raw_data.csv")

system("appcfg.py download_data  --url=http://twothirdsoftheaveragegame.appspot.com/_ah/remote_api --config_file=bulkloader.yaml --filename=raw_data.csv --kind=Guess")
