#!/usr/bin/env python3

import argparse
import kolmo

parser = argparse.ArgumentParser()
parser.add_argument('--target', dest='target', type=str)
args = parser.parse_args()

print(kolmo.name_by_content(args.target, {}))

