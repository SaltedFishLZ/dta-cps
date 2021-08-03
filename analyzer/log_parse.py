#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import sys
import time
import enum
import warnings

import rocket_parser

class ExecutionState(enum.Enum):
    Idle = 0
    StartPending = 1
    StartCommitted = 2
    Running = 3
    EndPending = 4
    EndComitted = 5


def log_parse(filename, start_stamp, end_stamp):
    assert type(start_stamp) == str, TypeError
    assert type(end_stamp) == str, TypeError

    print("=" * 64)
    print("Extracing [" + filename + "]")
    print("=" * 64)

    _f = open(filename, "r")
    line_count = 0

    # logs
    start_count = 0
    end_count = 0
    valid_start_count = 0 # stamps that are really committed / finished
    valid_end_count = 0 
    execution_count = 0
    execution_start_time = -1
    execution_end_time = -1

    # final results
    results = []

    # state
    state = ExecutionState.Idle

    while True: 
        # get next line from file 
        line = _f.readline()
        line_count += 1

        # if line is empty 
        # end of file is reached 
        if not line: 
            break

        # # debug
        # if start_count > 10:
        #     break

        # parse input
        cycles = rocket_parser.get_cycles(line)
        valid = rocket_parser.get_valid(line)
        inst = rocket_parser.get_inst(line)

        # -------------------------------- #
        #           matching FSM           #
        # -------------------------------- #

        if (state == ExecutionState.Idle or
            state == ExecutionState.StartPending
            ):
            # match start stamp
            if (start_stamp in line):
                # state transfer
                start_count += 1
                if (int(valid) != 0):
                    state = ExecutionState.StartCommitted
                    valid_start_count += 1
                else:
                    state = ExecutionState.StartPending
 
            # match end stamp
            elif (end_stamp in line):
                # state transfer
                end_count += 1
                if (int(valid) > 0):
                    raise ValueError("Cannot accpet end_stamp at {}, line:{}".format(
                                     state, line_count))
            else:
                pass
        
        elif (state == ExecutionState.EndPending or
              state == ExecutionState.Running
              ):
            # match start stamp
            if (start_stamp in line):
                # state transfer
                if (int(valid) > 0):
                    raise ValueError("Cannot accpet start_stamp at {}, line:{}".format(
                                     state, line_count))

            # match end stamp
            elif (end_stamp in line):
                # parse input
                cycles = int(rocket_parser.get_cycles(line))
                valid = int(rocket_parser.get_valid(line))
                inst = rocket_parser.get_inst(line)
                # state transfer
                end_count += 1
                if (int(valid) != 0):
                    state = ExecutionState.EndComitted
                    valid_end_count += 1
                else:
                    state = ExecutionState.EndPending
            else:
                pass

        elif (state == ExecutionState.StartCommitted):
            # state transfer
            state = ExecutionState.Running
            # log results
            execution_count += 1
            execution_start_time = int(cycles)

        elif (state == ExecutionState.EndComitted):
            # state transfer
            state = ExecutionState.Idle
            # log results
            execution_end_time = int(cycles)
            log_dict = {
                "execution_count": execution_count,
                "execution_start_time": execution_start_time,
                "execution_end_time": execution_end_time
                }
            results.append(log_dict)
            execution_start_time = -1
            execution_end_time = -1
        
        else:
            raise ValueError

        # -------------------------------- #



    print("finished!")
    print("line count {}".format(line_count))
    print("start count {}".format(start_count))
    print("end count {}".format(end_count))
    print("execution count {}".format(execution_count))
    _f.close() 

    return results




if __name__ == "__main__":

    filename = "test.log"

    results = log_parse(filename, start_stamp="pc=[80001088]", end_stamp="pc=[8000106c]")
    # print(results)

    execution_durations = []
    for log_dict in results:
        execution_start_time = log_dict["execution_start_time"]
        execution_end_time = log_dict["execution_end_time"]
        duration = execution_end_time - execution_start_time
        execution_durations.append(duration)
    print(execution_durations)
