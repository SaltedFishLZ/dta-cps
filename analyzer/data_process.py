import os
import sys
import glob
import pickle
import warnings
import argparse
import numpy as np

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

    data = collect_data(args.dataroot)

    boom_data = {}
    for k,v in data.items():
        print('Reaction k: ' + str(k))
        arr = np.array(v)
        leng = arr.shape[0]
        std = np.std(v) * 1 * 3 # 300% of var
        mean = np.mean(v) * 0.6 # 40% performance boost
        boom_data[k] = np.random.normal(mean, std, leng)
        # boom_data[k] = np.random.poisson(mean, leng)

    for k,v in boom_data.items():
        print(str(k) + ' WCET: ' + str(int(np.max(v))))
