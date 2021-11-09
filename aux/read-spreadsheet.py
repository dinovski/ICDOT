#!/usr/bin/env python3

# see https://pandas.pydata.org/pandas-docs/dev/user_guide/io.html#io-excel-reader

from datetime import datetime, date
import pandas as pd
import numpy as np
from collections import OrderedDict
from pprint import pprint
import json
import sys,argparse
from xlrd import XLRDError
need_sheets = ['required', 'recipient', 'donor', 'biopsy', 'histology', 'nanostring']
sheet_header_2nd_line = ['recipient','donor','nanostring']

debug = False


def parse_command_line():
    # Define parameters
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="This is a frobnicator")

    # Option parameters
    parser.add_argument("-V", "--verbose",  help="be verbose",
                        action="store_true")
    parser.add_argument("-d", "--debug",  help="debug",
                        action="store_true")

    # Positional parameter
    parser.add_argument('filename', metavar='FILE', help='file to process');
    args = parser.parse_args()

    return args


def read_icdot_excel(filename):
    try:
        xlsx = pd.ExcelFile(filename)
    except (FileNotFoundError,XLRDError) as e:
        sys.exit(str(e))

    output = OrderedDict()

    for s in need_sheets:
        data = None
        try:
            data = pd.read_excel(xlsx,s)
        except XLRDError:
            # Skip this missing sheet
            sys.exit("no sheet" + s)
            continue

        # In these sheets the headers are in the second row.
        # The first row contains something like "required/option".
        # The first row was read as the headers.
        # The second row was read as the first data line (index 0).
        # Set the column names and drop the second line:
        if s in sheet_header_2nd_line:
            data.columns = data.iloc[0].values
            data = data.drop([0])

        if debug:
            print("sheet = ", s)
            pprint(data)

        # Drop rows without meaningful data
        data = data.dropna(how='all')

        # Replace 'NAN' with None
        data = data.replace({np.nan: None})

        t = data.to_dict(orient='record',into=OrderedDict)

        output[s] = t

    return output


# From https://stackoverflow.com/a/22238613
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))



if __name__ == "__main__":
    args = parse_command_line()

    if args.verbose:
        print("File to process:", args.filename)

    debug = args.debug

    d = read_icdot_excel(args.filename)

    if debug:
        pprint(d)

    print(json.dumps(d, default=json_serial))
