#!/usr/bin/env python

from os import system, listdir, remove
from csv import reader, writer


class Player():
    """A class to hold the data if this is required"""
    def __init__(self, date, number, personal_url, author):
        self.numbers = {date: number}
        self.urls = {date: personal_url}
        self.author = author
        self.dates = [date]

    def last_guess(self):
        self.dates.sort()
        return self.numbers[self.dates[-1]]

    def last_url(self):
        self.dates.sort()
        return self.urls[self.dates[-1]]

download_raw_data = raw_input("Download raw data from app engine? (y/n) ")
if download_raw_data == "y":
    if "raw_data.csv" in listdir("./"):
        remove("raw_data.csv")

    system("appcfg.py download_data  --url=http://twothirdsoftheaveragegame.appspot.com/_ah/remote_api --config_file=bulkloader.yaml --filename=raw_data.csv --kind=Guess")

    clear_log_files = raw_input("Remove bulkloader log files? (y/n) ")
    if clear_log_files == "y":
        for f in listdir("./"):
            if "bulkloader-" in f:
                remove(f)

if "raw_data.csv" in listdir("./"):
    clean_data = raw_input("Write data_from_webapp.csv? (y/n) ")
    if clean_data == "y":  # If prompted to write a clean data file
        # Read in raw data
        f = open("raw_data.csv", "rb")
        data = reader(f)
        data = [row for row in data]
        f.close()
        data = data[1:]
        Player_Dict = {}  # Initiate a player dict
        for row in data:
            date = row[0]
            number = row[1]
            personal_url = row[2]
            author = row[3]
            if author in Player_Dict:  # If player has already guessed, add to dictionary
                Player_Dict[author].numbers[date] = number
                Player_Dict[author].urls[date] = personal_url
                Player_Dict[author].dates.append(date)
            else:  # If player has not guessed create data object.
                Player_Dict[row[3]] = Player(row[0], row[1], row[2], row[3])
        # Write data_from_webapp.csv
        f = open("data_from_webapp.csv", "wb")
        outfile = writer(f)
        outfile.writerow(["UserName", "url", "Guess", "Date", "NumberOfGuess"])
        for key in Player_Dict:
            plyr = Player_Dict[key]
            outfile.writerow([plyr.author, plyr.last_url(), plyr.last_guess(), plyr.dates[-1], len(plyr.dates)])
        f.close()

else:
    print "No raw_data.csv file found."
