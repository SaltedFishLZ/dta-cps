import pandas as pd
import numpy as np
import heapq as hq
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches

import plotly.figure_factory as ff 

ROWS = 60

# This is because I am storing weird stuff in the dictionary
class CompareWord:
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


df = pd.read_csv("EDF_data.csv", index_col="task-id")
heap = []
time = 0

# print(df.head())

ex_percent = np.sum(df['exec-time-worst'] / df['period'])
print(ex_percent)

# function to determing what is coming
def incoming_task(time):
    return df[time % df['period'] == 0]
    

def determine_exec_time(arr):
    # best, worst, average is not equal to 33% each time (not for task-id 1 anyway)
    # but it should be close enough
    return np.random.choice(arr, p = [.1, .1, .8])

def heap_func(row):
    exec_time = determine_exec_time(row.to_numpy()[1:4]) # Dont want period (index = 0) nor time (index = 4)

    deadline = row['period'] + row["time"]
    # print("heap func")
    heap_item = {
        "period": row['period'],
        "start_time": row["time"],
        "end_time": None,
        "deadline": deadline,
        "Error": False,
        "exec_time": exec_time,
        "ticks_remaining": exec_time,
        "Name": "start:{}-period:{}-deadline{}".format(row["time"], row['period'], deadline)
    }
    # print(heap_item)
    hq.heappush(heap, CompareWord(deadline, heap_item))


def run_scheduling(max_time):

    gantt_chart = pd.DataFrame(columns=["period", "start_time", "end_time", "deadline", "Error", "exec_time", "ticks_remaining", "Name"])

    for tick in range(max_time): # time loop
        incoming = incoming_task(tick)
        incoming["time"] = tick * np.ones(len(incoming), dtype=int)
        incoming = incoming

        # # Incoming tasks
        if len(incoming) != 0:
            # print(tick)
            incoming.apply(heap_func, axis = 1)

        # # Outgoing Task -- EDF can only pop one task at a time, but can add more than one task
        if (len(heap) > 0):
            item = hq.heappop(heap)
        else:
            print("nothing to pop as its zero")
            continue
        # print(item.getValue())
        # item.setTime(item.getValue()["ticks_remaining"] - 1)
        # print(item.getValue()["ticks_remaining"])
        
        if item.getValue()["deadline"] < tick:
            item.setError()
            # print("\n\n\t\tthere was an error here, This missed the deadline")
            # print(item.getValue())

        if item.getValue()["ticks_remaining"] == 0:
            item.setFinishTime(tick)
            gantt_chart.loc[len(gantt_chart)] = item.getValue()
            # print("completed!!")
        else:
            item.setTime(item.getValue()["ticks_remaining"] - 1)
            hq.heappush(heap, CompareWord(item.getTime(), item.getValue()))
        # except:
        #     pass
    return gantt_chart

gantt_chart = run_scheduling(ROWS)
# print(gantt_chart.head())

fig, ax_gnt = plt.subplots(figsize = (12, 8))

# for i, t in enumerate(gantt_chart["Name"]):
#     ax_gnt.broken_barh([(gantt_chart[i], gantt_chart["end_time"] - gantt_chart["start_time"]), (gantt_chart["name"], len(gantt_chart)), facecolors = ('tab:')])

plty = pd.DataFrame(columns = ["Task", "Start", "Finish", "Resource"])

# plty.columns = ["Task", "Start", "Finish", "Resource"]

# print(gantt_chart.head(ROWS))


plty["Resource"] = ["Critical" if x else "Not Critical" for x in gantt_chart['Error']]
plty['Task'] = gantt_chart["Name"]
plty['Start'] = gantt_chart["start_time"]
plty['Finish'] = gantt_chart["end_time"]
plty["Deadline"] = gantt_chart["deadline"]

# print(plty.head(ROWS))

critical_colors = {'Not Critical': 'rgb(0, 50, 98)', 'Critical': 'rgb(253, 181, 21)'}

x_seq = []

for i, row in plty.iterrows():
    # print(row["Start"], row["Finish"])
    tupe = (row['Start'], row['Finish'] - row['Start'])
    x_seq.append(tupe)
    # print(tupe, i)
    ax_gnt.broken_barh([tupe], (i, 3), facecolors = 'tab:red' if row['Resource'] == 'Critical' else 'tab:blue')
    ax_gnt.broken_barh([tupe], (i+1, 3), facecolors = 'white')
    # ax_gnt.axvline(x = row["Deadline"], ymin = 0, ymax = i + 3)

# print(x_seq)

# ax_gnt.broken_barh(x_seq, (0, 9), facecolors = 'tab:red' if True else 'tab:blue')

ax_gnt.set_yticks([ir + .5 for ir  in range(len(plty))])
ax_gnt.set_yticklabels(plty["Task"].to_numpy())

# ax_gnt.set_xticks([ir for ir in range(i)])
# ax_gnt.set_yticklabels(plty["Task"].to_numpy())

red_patch = mpatches.Patch(color='red', label='Task that failed to meet its deadline')
blue_patch = mpatches.Patch(color='blue', label='Task that met its deadline')

ax_gnt.grid(True)
# ax_gnt.set_ylim(0, 10)
# ax_gnt.set_xlim(0, 30)
plt.legend(handles = [red_patch, blue_patch])
plt.show()

# fig_plotly = ff.create_gantt(plty, colors = critical_colors, index_col = 'Resource', 
#     title = 'Gantt Chart', show_colorbar = True, bar_width = 0.4, showgrid_x=True, showgrid_y=True) 


# fig_plotly.show()


