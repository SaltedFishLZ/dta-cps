#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import sys
import time
import enum
import warnings

from common import match_regex

class ScanState(enum.Enum):
    Idle = 0
    FindStart = 1
    FindEnd = 2


def extract_stamp(filename, stamp_id=0):
    assert type(filename) == str, TypeError
    assert type(stamp_id) == int, TypeError

    print("=" * 64)
    print("Extracing [" + filename + "]")
    print("=" * 64)

    _f = open(filename, "r")
    line_count = 0

    # start_mark = "magic_start_stamp({})".format(stamp_id)
    # end_mark = "magic_end_stamp({})".format(stamp_id)

    start_mark = "# 149a{0:04x} <buf.".format(stamp_id + 1)
    end_mark = "# 249a{0:04x} <buf.".format(stamp_id + 1)

    start_stamp = None
    end_stamp = None

    # state
    state = ScanState.Idle

    while True: 
        # get next line from file 
        line = _f.readline()
        line_count += 1

        # if line is empty 
        # end of file is reached 
        if not line: 
            break

        if (state == ScanState.Idle):
            if (start_mark in line):
                state = ScanState.FindStart
            elif (end_mark in line):
                state = ScanState.FindEnd
            else:
                state = ScanState.Idle
        elif (state == ScanState.FindStart):
            # action
            regex = r"([0-9a-fA-FxX]+):([\s\t]+)([0-9a-fA-FxX]+)"
            match = match_regex(regex, line)
            assert (match is not None), ValueError
            if start_stamp is not None:
                warnings.warn("multiple start mark found!")
            start_stamp = match[0]
            start_stamp = "pc=[{}]".format(start_stamp)
            # state tranfer
            state = ScanState.Idle
        elif (state == ScanState.FindEnd):
            # action
            regex = r"([0-9a-fA-FxX]+):([\s\t]+)([0-9a-fA-FxX]+)"
            match = match_regex(regex, line)
            assert (match is not None), ValueError
            if end_stamp is not None:
                warnings.warn("multiple end mark found!")
            end_stamp = match[0]
            end_stamp = "pc=[{}]".format(end_stamp)
            # state tranfer
            state = ScanState.Idle

    _f.close() 

    return (start_stamp, end_stamp)



if __name__ == "__main__":

    filename = "test.dump.annot"

    (start_stamp, end_stamp) = extract_stamp(filename)
    print("(start_stamp, end_stamp) = ", (start_stamp, end_stamp))
