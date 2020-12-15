#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import sys
import pickle
import warnings
import argparse


from extract_stamp import extract_stamp
from log_parse import log_parse
from timing import get_execution_durations



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", metavar="DIR", type=str,
                        help="folder path for")
    parser.add_argument("name", metavar='N', type=str,
                        help="binary name, assume other files have the same name with different suffixs")
    parser.add_argument("--dump", metavar="D", type=str,
                        help="dump to certain files")

    args = parser.parse_args()

    prefix = os.path.join(args.dir, args.name)

    # get annotations
    annot_fpath = "{}.dump.annot".format(prefix)
    (start_stamp, end_stamp) = extract_stamp(annot_fpath)
    print("(start_stamp, end_stamp) = ", (start_stamp, end_stamp))

    # parse logs with annotations
    log_fpath = "{}.log".format(prefix)
    logs = log_parse(log_fpath, start_stamp=start_stamp, end_stamp=end_stamp)

    # get execution durations
    execution_durations = get_execution_durations(logs)

    print(execution_durations)

    if (args.dump is not None):
        print(args.dump)
        dump_fpath = "{}.timing.pkl".format(prefix)
        _dump_f = open(dump_fpath, "wb")
        pickle.dump(execution_durations, _dump_f)
        _dump_f.close()
