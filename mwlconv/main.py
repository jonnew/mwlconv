#!/usr/bin/python

import argparse as ap
from .oat2xpos import Oat2xpos
from .oe2xtt import Oe2xtt


def main():

    # Parse command line options
    parse = ap.ArgumentParser()
    parse.add_argument("routine", help="Conversion type to perform", type=str)
    parse.add_argument("-i", "--input", nargs='*', help="File(s) to convert. Defaults to stdin.", type=str)
    parse.add_argument("-o", "--output", help="Output file. Defaults to stdout.", type=str)
    parse.add_argument("-s", "--timescale", help="Timescale muptiplier.", type=float, required=True)
    parse.add_argument("-I", "--invert", help="Invert data around 0. Defaults to True.", type=bool)
    parse.set_defaults(invert=True)
    args = parse.parse_args()

    # Swich on the type to call the correct tool
    if args.routine == "oat2pos":

        if args.input:
            converter = Oat2xpos(*args.input) 
            converter.parse(args.timescale)

        converter.dump(args.output)

    elif args.routine == "oe2tt":

        if args.input:
            converter = Oe2xtt(*args.input)
            converter.parse(args.invert)

        converter.dump(args.output)

    else:
        raise ValueError('Specified converion routine is not supported.')

if __name__ == '__main__':
    main()
