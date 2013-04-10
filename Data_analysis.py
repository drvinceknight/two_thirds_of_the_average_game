#!/usr/bin/env python
from __future__ import division
import csv
import matplotlib.pyplot as plt
import os
import sys

arguments = sys.argv

if len(arguments) == 1:
    sys.exit("""

Please pass a csv as an argument to Data_analysis:

    ./Data_analysis.py CSV_FILE_OR_DIRECTORY

             """)


def analyse_given_data_set(data, file_name):
    # Confirm that data has been read and output properties of file
    number_of_players = len(data)
    print "Data file read with %s players" % number_of_players

    # Calculating mean of guesses
    first_guess_mean = sum([e[1] for e in data]) / number_of_players
    second_guess_mean = sum([e[2] for e in data]) / number_of_players
    print "Mean of the first guess: %s so 2/3rds of mean is: %s" % (first_guess_mean, 2 * first_guess_mean / 3)
    print "Mean of the second guess: %s so 2/3rds of mean is: %s" % (second_guess_mean, 2 * second_guess_mean / 3)

    first_guess_distance = [abs(e[1] - 2 * first_guess_mean / 3)for e in data]
    second_guess_distance = [abs(e[1] - 2 * second_guess_mean / 3)for e in data]
    winning_first_guess = data[first_guess_distance.index(min(first_guess_distance))][1]
    winning_second_guess = data[second_guess_distance.index(min(second_guess_distance))][1]
    print "Winning first guess: %s" % winning_first_guess
    print "Winning second guess: %s" % winning_second_guess

    # Plot histograms of guesses using matplotlib
    plt.figure()
    plt.hist([e[1] for e in data], bins=20, label='First Guess', normed='True')
    plt.hist([e[2] for e in data], bins=20, alpha=.75, label='Second Guess', normed='True')
    plt.title("Two thirds of the average game ($N=%s$)." % number_of_players)
    plt.xlabel("Guess")
    plt.ylabel("Probability")
    max_y = plt.ylim()[1]
    plt.vlines(winning_first_guess, 0, max_y, label='Winning first Guess: %s' % winning_first_guess, color='blue')
    plt.vlines(winning_second_guess, 0, max_y, label='Winning Second Guess: %s' % winning_second_guess, color='green')
    plt.ylim(0, max_y)
    plt.xlim(0, 100)
    plt.legend()
    plt.savefig("Results_for_%s.png" % file_name)


def read_csv_file(csv_file):
    print "Reading %s." % csv_file
    outfile = open(csv_file, "rb")
    data = csv.reader(outfile)
    data = [e for e in data]
    data = [[e[0], round(eval(e[1])), round(eval(e[2]))] for e in data[1:]]
    return data

# Read in data
if os.path.isdir(arguments[1]):
    print "Reading directory %s." % arguments[1]
    csv_files = [f for f in os.listdir(arguments[1]) if f[-4:] == ".csv"]
    print "%s csv files found." % len(csv_files)
    for f in csv_files:
        print "\n"
        data = read_csv_file(arguments[1] + "/" + f)
        file_name = f[:f.index(".csv")]
        analyse_given_data_set(data, file_name)
else:
    file_name = arguments[1][arguments[1].rindex("/") + 1: arguments[1].index(".csv")]
    data = read_csv_file(arguments[1], file_name)
    analyse_given_data_set(data)
