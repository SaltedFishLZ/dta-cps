import pandas as pd
import numpy as np

edf_data = pd.read_excel('example.xlsx')
# display(edf_data)
# You can make the function return a list of dicts (each dict has task id, execution times and missing deadline times)
task_id = list(edf_data['task-id'])
n_tasks = len(task_id)
exc_time = list(edf_data['exec-time-best'])
period = list(edf_data['period'])
total_timeline = np.prod(edf_data['period'].unique())

task_timeline = []
time_left = []
tasks_left = []
min_period = 0
time = 0
to_choose_from = []
executed = []
while time < total_timeline:
    if (len(executed) == 3):
        executed = []
    for i in range(n_tasks):
        if((time + exc_time[i]) % period[i] > (time + period[i]) % period [i]):
            print("task {} deadline missed at time: {}".format(i + 1,time+exc_time[i]))
    time_left = []
    to_choose_from = []
    for p in period:
        time_left.append(p - time % p)
    for i in range(n_tasks):
        if(i + 1 not in executed):
            to_choose_from.append(time_left[i])
    index_task = time_left.index(min(to_choose_from))
    task_timeline.append('task: {} at time: {}'.format(task_id[index_task], time + exc_time[index_task]))
    executed.append(task_id[index_task])
    time+=1
print(task_timeline)