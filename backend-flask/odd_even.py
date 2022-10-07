#!/usr/bin/python3
"""
The goal of this project is to create an application that takes in user typed
input, and uses good UX (up to you) to display the longest "even" or "odd"
streak of letters. Evenness for the letters alternates with a = even, b = odd,
c = even, d = odd etc.

A few gotchas:

Whitespace neither counts for a streak, nor breaks a streak
Non-alphabetic characters including numbers break a streak
Capitalization does not matter
Underneath the displayed string, please put the total streak count

Here are some examples of what a finished product could look like.
"""

from copy import copy
import string
from itertools import groupby
from flask import Flask, jsonify, request, escape

from flask_cors import CORS

# ——————————————— VIRTUAL DATABASE —————————————————————
LOCAL_DB = [
    {
        "id": "1",
    },
]

DEFAULT_RESPONSE = {'markdown': '', 'maxx': 0}

EVENS = [
    letter for x,
    letter in enumerate(
        string.ascii_lowercase) if x % 2 == 0]
ODDS = [
    letter for x,
    letter in enumerate(
        string.ascii_lowercase) if x % 2 == 1]
# ODDS = [letter if x % 2 == 1 for x, letter in
# enumerate(string.ascii_lowercase)]

app = Flask(__name__)
CORS(app)

# ———————————— SERVICE FUNCTIONS —————————————


def check_string(orignal_string):
    """ Analyze string for streaks """
    if not len(orignal_string):
        # empty input
        return DEFAULT_RESPONSE

    a_string = copy(orignal_string)
    state = 'N/A'
    markdown_string = ''
    streaks = []

    # Lowcase, then remove spaces and mark them with special char ('X')
    a_string = a_string.lower().replace(" ", "X")

    # Replace all streak breaking chars with spaces — group dividers
    a_string = "".join([letter
                        if letter in string.ascii_letters else " "
                        for letter in a_string])

    # Encode odds and evens with 1/0
    odds_even = ""
    for letter in a_string:
        if letter in EVENS:
            odds_even += "0"
        elif letter in ODDS:
            odds_even += "1"
        else:
            odds_even += letter

    # Group string by streaks
    clean_groups = []  # here all substrings
    for char, substring in groupby(odds_even):
        lenx = sum(1 for i in substring)  # length of the substring
        count = lenx if char not in ['X', ' '] else 0  # Count only correct chars
        # build a list with each group details
        clean_groups.append((char, count, lenx))

    # Next — combine similar streaks that may be split by spaces (marked 'X')
    joined_groups = []
    groups_qty = len(clean_groups)
    idx = 0
    # for _ in range(groups_qty):
    while idx < groups_qty:
        char, count, lenx = clean_groups[idx]
        for idy in range(idx + 1, groups_qty):
            char_y, count_y, leny = clean_groups[idy]
            if (char_y != char) and (char_y != 'X'):
                break
            else:
                count += count_y
                lenx += leny
                idx += 1  # skip the next group then
        joined_groups.append((char, count, lenx))
        # if idx < groups_qty - 1:
        idx += 1

    # Find maximum streak count
    counts_list = [count for char, count, lenx in joined_groups if char != ' ']
    if len(counts_list):
        maxx = max(counts_list)
    else:
        # Something wrong with input string, no max??? exit...
        return DEFAULT_RESPONSE

    # Add fancy formatting
    position = 0  # position in the input string
    for charx, count, lenx in joined_groups:
        # Sanitize input string (no html!)
        group_sub = str(escape(orignal_string[position:position + lenx]))
        # Check if max streak, skip special chars
        if (charx != ' ') and (count == maxx):
            state = charx  # Type of group odd/even
            streaks.append(group_sub)  # If more than one max streak
            markdown_string += '<mark>' + group_sub + '</mark>'  # Add markdown
            # markdown_string += group_sub   # ** DEBUG **
        else:
            # Just add the group to output
            markdown_string += group_sub
        position += lenx

    return {'input': orignal_string,
            'markdown': markdown_string,
            'odds_even': odds_even,
            'clean_groups': clean_groups,
            'joined_groups': joined_groups,
            'maxx': maxx,
            'state': state,
            'streak': streaks,
            }


# ——————————————— ENDPOINTS ———————————————————
@app.route("/odd-even/", methods=['GET'])
def computers():
    """ Endpoint handler

        Request example:
            /odd-even/?input=<string> """
    data = DEFAULT_RESPONSE

    if len(request.args):
        # There are some arguments, filter data by the arguments
        for arg in request.args:
            # Filter results by each argument value
            argument_value = request.args.get(arg, None)

            data = check_string(argument_value)

    else:
        # Default case (no arguments)
        pass  # ** used for debug **

    return jsonify(data)  # Reply just data


# ————————————— ERROR HANDLER ————————————————
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"result": "wrong path"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=22045)
