import plotly
plotly.tools.set_credentials_file(username='fitcommunity', api_key='2RRiubR76pvXmCbFI8r3')
plotly.__version__

from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF
from IPython.display import HTML

import numpy as np
import pandas as pd

import csv

with open('plotly-sleep.csv') as csvfile1:
    readCSVsleep = csv.reader(csvfile1,delimiter=',')
    sleephours = []

    for row in readCSVsleep:
        sleephour = row[2]
        sleephours.append(sleephour)

with open('plotly_activities.csv') as csvfile2:
    readCSVactivities = csv.reader(csvfile2,delimiter=',')
    dates = []
    caloriesburned = []
    steps = []

    for row in readCSVactivities:
        date = row[0]
        calorieburned = row[1]
        step = row[2]
        dates.append(date)
        caloriesburned.append(calorieburned)
        steps.append(step)


trace1 = go.Scatter(
    x=dates,
    y=caloriesburned, # Data
    name='Calories Burned',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4)
)
trace2 = go.Scatter(
    x=dates,
    y=steps, # Data
    name='Steps taken',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4)
)
trace3 = go.Scatter(
    x=dates,
    y=sleephours, # Data
    name='Hours slept ',
    line = dict(
        color = ('rgb(205, 12, 24)'),
        width = 4)
)
fig = tools.make_subplots(rows=1,cols=3)
fig.append_trace(trace1,1,1)
fig.append_trace(trace2,1,2)
fig.append_trace(trace3,1,3)

py.iplot(fig, filename='CSV Data')


first_plot_url = py.plot(fig, auto_open=False, filename='CSV Data')
print(first_plot_url)

html_string = '''
<html>

<head>
<style> body{ margin:0 100; background:whitesmoke; } </style>
</head>

<body>
<h1>Graphs</h1>
    <h2>Section 1: Graphs from CSV Data </h2>
        <iframe width="1000" height="550" frameborder="0" seamless="seamless" scrolling="no" \
src="''' + first_plot_url + '''.embed?width=800&height=550"></iframe>
</body>

</html>
'''

f = open("index.html","w")
f.write(html_string)
f.close()
