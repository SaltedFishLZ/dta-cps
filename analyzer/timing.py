
#!/usr/bin/python3
# -*- coding: UTF-8 -*-

def get_execution_durations(logs):
    assert type(logs) == list, TypeError

    execution_durations = []
    for log_dict in logs:
        execution_start_time = log_dict["execution_start_time"]
        execution_end_time = log_dict["execution_end_time"]
        duration = execution_end_time - execution_start_time
        execution_durations.append(duration)

    return execution_durations
