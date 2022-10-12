#!/usr/bin/python3
"""
TEST application: test the endpoint.

Example (argument — an input file with test sequences):

  tests.py tests.json 
"""
import requests
from pathlib import Path
import argparse
import json


BASE_URL = " https://www.1axm.com/odd-even/"
API_CALL = BASE_URL + "?input={sequence}"


def test_rounds(input_sequences):
    for sequence in input_sequences:
        test_sequence = list(sequence.keys())[0]
        response = requests.get(API_CALL.replace("{sequence}", test_sequence))
        output = response.json()
        try:
            print(f"{test_sequence} Expected: {sequence[test_sequence]} | Received: {output['maxx']}")
            assert output['maxx'] == sequence[test_sequence]
        except Exception as e:
            print(f"^ —— Assertion failed [{e}]")
    return


def main():

    parser = argparse.ArgumentParser(
        usage=__doc__
    )

    # parser.add_argument(
    #     "-p", "--prefix",
    #     dest="prefix",
    #     default="",
    #     help="A prefix for the message",
    #     required=False,
    # )

    parser.add_argument(
        "file",
        help="input filename containing test sequences",
        metavar="PATH"
    )

    args = parser.parse_args()
    
    if Path(args.file).is_file():
        print("File exist, committing tests...")
        with open(args.file, "r") as f:
            sequences = json.load(f)
            num_of_sequence = len(sequences)
            if num_of_sequence:
                test_rounds(sequences)
    else:
        print(f"File {args.file} not exist")
        return
    
    print(f'Committed {num_of_sequence} tests.')
    return


if __name__ == "__main__":
    main()
