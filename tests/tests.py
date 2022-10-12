#!/usr/bin/python3
"""
TEST application: test the endpoint.

Example (argument — an input file with test sequences):

  tests.py tests.json 
"""
import requests
from pathlib import Path
import argparse


BASE_URL = " https://www.1axm.com/odd-even/"
API_CALL = BASE_URL + "?input={sequence}"


def test_rounds(input_sequences):
    for test in input_sequences:
        response = requests.get(API_CALL.replace("{sequence}", test['input']))
        output = response.json()
        assert output['maxx'] == test['expected']
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
        print("File exist, commiting tests...")
    else:
        print(f"File {args.file} not exist")
        return
    
    print(f'Committing {len()} tests ')
    return


if __name__ == "__main__":
    main()
