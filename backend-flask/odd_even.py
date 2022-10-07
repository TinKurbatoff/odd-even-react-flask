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
from flask import Flask, jsonify, request

from flask_cors import CORS

# ——————————————— VIRTUAL DATABASE —————————————————————
LOCAL_DB = [
    {
        "id": "1",
    },
]

EVENS = [letter for x, letter in enumerate(string.ascii_lowercase) if x % 2 == 0]
ODDS = [letter for x, letter in enumerate(string.ascii_lowercase) if x % 2 == 1]
# ODDS = [letter if x % 2 == 1 for x, letter in enumerate(string.ascii_lowercase)]

app = Flask(__name__)
CORS(app)

# ———————————— SERVICE FUNCTIONS —————————————
def check_string(a_string):
    """ Analyze string for streaks """
    orignal_string = copy(a_string)
    state = 'N/A'
    markdown_string = ''
    
    # Lower chars then remove spaces and mark them with special char within ASCII letters set
    a_string = a_string.lower().replace(" ", "X") 
    
    # Replace all breaking chars by a space
    a_string = "".join([letter if letter in string.ascii_letters else " " for letter in a_string])
    
    # Analyze
    odds_even = ""
    for letter in a_string:
        if letter in EVENS:
            odds_even += "0"
        elif letter in ODDS:
            odds_even += "1"
        else:
            odds_even += letter
    
    # Group string by streaks
    # odds_even = odds_even.replace("X","")
    # clean_groups = [] # here all groups for indication
    # for n, c in groupby(odds_even):
    #    num, count = n,sum(1 for i in c)
    #    clean_groups.append((num, count))    
    
    # Find the longest streak and its position
    max_streak_len = 0
    max_streak_position = 0
    current_streak_type = None
    current_streak_len = 0
    for x, letter in enumerate(odds_even):
        if letter == "X":
            # Skip spaces (were replaced with "X")
            pass
        elif (letter == ' ') or (letter != current_streak_type):
            # Group end!
            if current_streak_len > max_streak_len:
                # Max group!
                max_streak_len = current_streak_len
                max_streak_position = x - current_streak_len
                state = current_streak_type
            
            if letter == ' ':
                # Group devider — (' ' — non-alphabetical)
                current_streak_type = None
                current_streak_len = 0
            else:
                # Group dividers (odds & even)
                current_streak_type = letter
                current_streak_len = 1
        else:
            # Just one more symbol
            current_streak_len += 1
    

    if max_streak_len:
        markdown_string = orignal_string[:max_streak_position] + \
                    '<mark>' + orignal_string[max_streak_position: max_streak_position + max_streak_len] + \
                    '</mark>' + orignal_string[max_streak_position + max_streak_len:]
    return {'input': orignal_string, 
            'markdown': markdown_string,
            'odds_even': odds_even, 
            # 'clean_groups': clean_groups,
            'maxx': max_streak_len, 
            'x': max_streak_position, 
            'y': max_streak_position + max_streak_len, 
            'max_streak_position': max_streak_position,
            'streak': orignal_string[max_streak_position: max_streak_position + max_streak_len], 
            'state': state
            }


# ——————————————— ENDPOINTS ———————————————————
@app.route("/odd-even/", methods=['GET'])
def computers():
    """ Endpoint handler
        
        Request example:
            /odd-even/?input=<string> """
    data = [0, 0]

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
