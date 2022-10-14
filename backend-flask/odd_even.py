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
from flask import Flask, jsonify, request, escape

from flask_cors import CORS

# ——————————————— VIRTUAL DATABASE —————————————————————
DEFAULT_RESPONSE = {'markdown': '', 'maxx': 0}

app = Flask(__name__)
CORS(app)  # CORS handler

# ———————————— SERVICE FUNCTIONS —————————————


def check_string(a_string):
    """ Analyze string for streaks """
    if not len(a_string):
        # empty input
        return DEFAULT_RESPONSE

    joined_groups = []
    streaks = []
    maxx = 0
    current_group_len = 0 
    current_group_chars = 0
    current_group_start = 0
    current_group_type = None

    for idx, a_char in enumerate(a_string):
        if " " == a_char:
            current_group_chars += 1
        elif a_char.isalpha():
            group_type = ord(a_char) % 2  # Get type odd/even
            if group_type == current_group_type:
                current_group_chars += 1
                current_group_len += 1
            else:
                if current_group_chars:
                    # Skip empty groups
                    joined_groups.append({
                        'streak': a_string[current_group_start: current_group_start + current_group_chars], 
                        'type': current_group_type, 
                        'length': current_group_len, 
                        'chars': current_group_chars
                        })
                current_group_type = ord(a_char) % 2
                current_group_chars = 1
                current_group_len = 1
                current_group_start = idx

            if current_group_len > maxx:
                maxx = current_group_len

        else:
            group_type = None
            current_group_len = 0
    
    joined_groups.append({
        'streak': a_string[current_group_start: current_group_start + current_group_chars], 
        'type': current_group_type, 
        'length': current_group_len, 
        'chars': current_group_chars
        })
    # streaks = [a_string[maxx_start:maxx_length]]

    # Build output
    markdown_string = ''
    for group in joined_groups:
        group_streak = group['streak']
        if maxx == group['length']:
            # Max
            markdown_string += '<mark>' + group_streak + '</mark>'
            streaks.append(group_streak)
        elif 0 == group['type']:
            # Odd, not max
            markdown_string += '<odd-mark>' + group_streak + '</odd-mark>'
        elif 1 == group['type']:
            # Even, not max
            markdown_string += '<even-mark>' + group_streak + '</even-mark>'
        else:
            # Other symbols
            markdown_string += group['streak']

    return {'input': a_string,
            'markdown': markdown_string,
            'joined_groups': joined_groups,
            'maxx': maxx,
            'streak': streaks,
            }


# ——————————————— ENDPOINTS ———————————————————
@app.route("/odd-even/", methods=['GET'])
def odd_even():
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
