import os
import sys
import glob
import pickle
import warnings
import argparse

from common import match_regex

def collect_data(dataroot, quiet=False):
    assert type(dataroot) == str, TypeError

    pickle_fpaths = glob.glob(dataroot + "/**/*.pkl", recursive=True)

    # scan for stamp ids and corresponding dumped rsults
    stamp_fpath_dict = {}
    for fpath in pickle_fpaths:
        _sid = match_regex(r"sid_(\d+).pkl", fpath)
        if ((_sid is not None) and (type(_sid)) == str):
            _sid = int(_sid)
            if _sid in stamp_fpath_dict:
                stamp_fpath_dict[_sid] += [fpath, ]
            else:
                stamp_fpath_dict[_sid] = [fpath, ]

    # collect data from different experiments
    stamp_results_dict = {}
    for _sid in stamp_fpath_dict:
        final_results = []
        result_fpaths = stamp_fpath_dict[_sid]
        for _fpath in result_fpaths:
            _f = open(_fpath, "rb")
            _result = pickle.load(_f)
            _f.close()
            final_results += _result
        print(final_results)
        stamp_results_dict[_sid] = final_results

    print(stamp_results_dict)
    # returned dict is unordered, you need to sort the keys
    # then use it
    return(stamp_results_dict)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataroot", metavar="DIR", type=str,
                        help="experiment data root")
    args = parser.parse_args()

    collect_data(args.dataroot)
