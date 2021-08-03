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
    parser.add_argument("--sid", nargs='+', type=int,
                        help='stamp id', required=False)
    parser.add_argument("--dump", "-d", action="store_true",
                        help="dump to certain files")
    # parser.add_argument("--dump", metavar="D", type=str,
    #                     help="dump to certain files")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="disable printing results")

    args = parser.parse_args()

    print(args.sid)


    prefix = os.path.join(args.dir, args.name)

    # check all possible stamp ids, default 0
    stamp_ids = args.sid
    if (stamp_ids is None):
        stamp_ids = [0, ]
    if (len(stamp_ids) == 0):
        stamp_ids = [0, ]

    for _sid in stamp_ids:

        # get annotations
        annot_fpath = "{}.dump.annot".format(prefix)
        (start_stamp, end_stamp) = extract_stamp(annot_fpath, stamp_id=_sid)
        print("(start_stamp, end_stamp) = ", (start_stamp, end_stamp))

        if (start_stamp is None or
            end_stamp is None):
            warnings.warn("cannot find magic stamp id {}".format(_sid))
        else:
            # parse logs with annotations
            log_fpath = "{}.log".format(prefix)
            logs = log_parse(log_fpath, start_stamp=start_stamp, end_stamp=end_stamp)

            # get execution durations
            execution_durations = get_execution_durations(logs)

            if (args.quiet is not True):
                print("=" * 64)
                print("stamp id {}".format(_sid))
                print("=" * 64)
                print(execution_durations)

            if (args.dump is True):
                print(args.dump)
                dump_fpath = "{}.sid{}.pkl".format(prefix, _sid)
                _dump_f = open(dump_fpath, "wb")
                pickle.dump(execution_durations, _dump_f)
                _dump_f.close()
