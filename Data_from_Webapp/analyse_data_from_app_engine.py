#!/usr/bin/env python
from __future__ import division
import matplotlib.pyplot as plt
from sys import argv
from os import listdir
import csv


def analyse_given_data_set(data):
    # Confirm that data has been read and output properties of file
    number_of_players = len(data)
    print "Data file read with %s players" % number_of_players

    # Calculating mean of guesses
    first_guess_mean = sum([e[1] for e in data]) / number_of_players
    print "Mean of the guess: %s so 2/3rds of mean is: %s" % (first_guess_mean, 2 * first_guess_mean / 3)

    first_guess_distance = [abs(e[1] - 2 * first_guess_mean / 3)for e in data]
    winning_first_guess = data[first_guess_distance.index(min(first_guess_distance))][1]
    print "Winning guess: %s" % winning_first_guess

    # Display winner
    print "The winning user name(s) are/is:"
    for e in data:
        if e[1] == winning_first_guess:
            print "\t" + e[0]
            print "\t\t" + e[0] + " guessed " + e[4] + " time(s) with the last guess on the " + e[3] + " (with url: " + e[2] + ")"

    # Plot histograms of guesses using matplotlib
    plt.figure()
    plt.hist([e[1] for e in data], bins=20, label='Guess', normed='True')
    plt.title("Two thirds of the average game ($N=%s$)." % number_of_players)
    plt.xlabel("Guess")
    plt.ylabel("Probability")
    max_y = plt.ylim()[1]
    plt.vlines(winning_first_guess, 0, max_y, label='Winning Guess: %s' % winning_first_guess, color='blue')
    plt.ylim(0, max_y)
    plt.xlim(0, 100)
    plt.legend()
    plt.savefig("Results_for_webapp.png")


def read_csv_file(csv_file):
    print "Reading %s." % csv_file
    outfile = open(csv_file, "rb")
    data = csv.reader(outfile)
    data = [e for e in data]
    data = [[e[0], eval(e[2]), e[1], e[3], e[4]] for e in data[1:]]
    return data


data_from_web_app = "data_from_webapp.csv"
if len(argv) > 1 and argv[1] in listdir("/"):
    data_from_web_app = argv[1]

data = read_csv_file(data_from_web_app)
analyse_given_data_set(data)
