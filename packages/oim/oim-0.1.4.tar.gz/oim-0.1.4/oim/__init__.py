#!/usr/bin/env python
import json
import argparse


def compress(jsonfile):
    with open(jsonfile, 'r') as f:
        orig = json.load(f)
        print orig


def uncompress(jsonfile):
    with open(jsonfile, 'r') as f:
        compressed = json.load(f)
        print compressed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--uncompress')
    parser.add_argument('jsonfile')
    args = parser.parse_args()

    if args.uncompress:
        uncompress(args.jsonfile)
    else:
        compress(args.jsonfile)


if __name__ == '__main__':
    main()
