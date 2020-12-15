import pandas as pd
import numpy as np
import heapq as hq
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches

import plotly.figure_factory as ff 


# This is because I am storing weird stuff in the dictionary
class CompareWord:
    """
    Class to implement a comparator to the incoming tasks.

    Because this is EDF, we obviously prioritize the deadline first, but then
    some decisions must be made. Here, to brake ties the following rank is implemented:
        1) deadline
        2) fewest ticks remaining in the task
        3) When the task was put in the scheduler
    """

    def __init__(self , deadline, value):
        self.deadline = deadline
        self.value = value


    def __lt__(self, other):   #To override > operator
        # Normal -> Choose the soonest Deadline
        if self.deadline != other.deadline:
            return self.deadline < other.deadline

        # Same deadline -> Choose the fewest ticks remaining
        elif self.deadline == other.deadline and self.value["ticks_remaining"] != other.value["ticks_remaining"]:
            return self.value["ticks_remaining"] < other.value["ticks_remaining"]

        # Same deadline and same ticks remaining -> choose the one that started sooner
        else:
            return self.value["start_time"] < other.value["start_time"]


    def __gt__(self , other):  #To override < operator
        # Normal -> Choose the soonest Deadline
        if self.deadline != other.deadline:
            return self.deadline > other.deadline

        # Same deadline -> Choose the fewest ticks remaining
        elif self.deadline == other.deadline and self.value["ticks_remaining"] != other.value["ticks_remaining"]:
            return self.value["ticks_remaining"] > other.value["ticks_remaining"]

        # Same deadline and same ticks remaining -> choose the one that started sooner
        else:
            return self.value["start_time"] > other.value["start_time"]

    """
    Basic class getter and setters to directly modify the value object 
    """

    def getTime(self):
        return self.deadline
    
    def getValue(self):
        return self.value
    
    def setTime(self, number):
        self.value["ticks_remaining"] = number
    
    def setError(self):
        self.value["Error"] = True
    
    def setFinishTime(self, number):
        self.value["end_time"] = number


# function to determing what is coming
def incoming_task(time, df):
    """
    Function to determing whats coming this tick. 
    When the mod is zero, the period is such that there is an incoming task to the scheduler
    """
    return df[time % df['period'] == 0]
    

def determine_exec_time(arr):
    """
    best, worst, average is not equal to 33% each time (not for task-id 1 anyway)
    but it should be close enough

    params - arr - 1d array of numbers
    returns - number - a single number chosen at random to act as the number of ticks needed to complete the task

    """
    return np.random.choice(arr)

def heap_func(row, time, t_start = 1, t_end = 4):
    """
    function to create the heap object and put it on the heap

    params - row - with objects period, time, and a way to derive a numpy array for worst, average, and best execution times
        to the be chosen
    
    returns - void? - meant to be only in a pandas apply function

    """
    exec_time = determine_exec_time(row.to_numpy()[t_start:t_end]) # Dont want period (index = 0) nor time (index = 4)

    deadline = row['period'] + time
    heap_item = {
        "period": row['period'],
        "start_time": time,
        "end_time": None,
        "deadline": deadline,
        "Error": False,
        "exec_time": exec_time,
        "ticks_remaining": exec_time,
        "Name": "start:{}-period:{}-deadline{}".format(time, row['period'], deadline)
    }

    hq.heappush(heap, CompareWord(deadline, heap_item))


def run_scheduling(max_time, df, t_start = 1, t_end = 4):
    """
    The scheduling loop, to be plotted in a gantt chart

    params - max time - number of time ticks this is supposed to run for
           df - dataframe of task id, period, worst, average, and best execution times
    
    returns df - a dataframe with the columns period, start time, end time, deadline, error, execution time, ticks remaining, and name of the task
    """

    gantt_chart = pd.DataFrame(columns=["period", "start_time", "end_time", "deadline", "Error", "exec_time", "ticks_remaining", "Name"])

    for tick in range(max_time): # time loop
        incoming = incoming_task(tick, df)
        # incoming["time"] = tick * np.ones(len(incoming), dtype=int)
        # incoming = incoming

        # Incoming tasks
        if len(incoming) != 0:
            incoming.apply(heap_func, axis = 1, args = (tick, t_start, t_end))

        # # Outgoing Task -- EDF can only pop one task at a time, but can add more than one task
        if (len(heap) > 0):
            item = hq.heappop(heap)
        else:
            print("nothing to pop as its zero")
            continue

        if tick-1 > item.getValue()['deadline']:
            print(tick, item.getValue()['deadline'])
            item.setError()

        if item.getValue()["ticks_remaining"] == 0:
            item.setFinishTime(tick)
            gantt_chart.loc[len(gantt_chart)] = item.getValue()
        else:
            item.setTime(item.getValue()["ticks_remaining"] - 1)
            hq.heappush(heap, CompareWord(item.getTime(), item.getValue()))
    return gantt_chart

def plot_gantt(df):
    """
    The code to plot and create a Gantt Chart of the data. 

    params - df - the specific output of run_scheduling

    returns - void? - a matplotlib figure is generated, but besides that nothing is generated. 
    """
    fig, ax_gnt = plt.subplots(figsize = (12, 8))
    plty = pd.DataFrame(columns = ["Task", "Start", "Finish", "Resource"])
    plty["Resource"] = ["Critical" if x else "Not Critical" for x in df['Error']]
    plty['Task'] = df["Name"]
    plty['Start'] = df["start_time"]
    plty['Finish'] = df["end_time"]
    plty["Deadline"] = df["deadline"]
    for i, row in plty.iterrows():
        tupe = (row['Start'], row['Finish'] - row['Start'])
        ax_gnt.broken_barh([tupe], (i, 3), facecolors = '#FDB515' if row['Resource'] == 'Critical' else '#003262')
        ax_gnt.broken_barh([tupe], (i+1, 3), facecolors = 'white')

    ax_gnt.set_yticks([ir + .5 for ir  in range(len(plty))])
    ax_gnt.set_yticklabels(plty["Task"].to_numpy())

    red_patch = mpatches.Patch(color='#FDB515', label='Task that failed to meet its deadline')
    blue_patch = mpatches.Patch(color='#003262', label='Task that met its deadline')

    ax_gnt.grid(True)
    plt.legend(handles = [red_patch, blue_patch])
    plt.show()

def main(path_to_csv = "scheduler/EDF_data.csv", TICKS = 250):
    """
    main function to run everything. I think this is what was wanted?

    params - path_to_csv - string, the path to the csv of the data. 
            TICKS - number, the number of ticks the scheduling algo is supposed to run for

    returns - void
    """


    df = pd.read_csv(path_to_csv, index_col="task-id")
    global heap
    heap = [] 

    ex_percent = np.sum(df['exec-time-worst'] / df['period'])
    print("this will always work if this is less than one:\t", ex_percent)


    gantt_chart = run_scheduling(TICKS, df)
    plot_gantt(gantt_chart)

if __name__ == '__main__':
    main()