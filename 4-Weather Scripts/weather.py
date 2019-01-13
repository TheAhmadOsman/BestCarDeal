import requests
import re
from math import ceil

# states = {}
# with open("weatherstates.txt") as f:
#     for line in f:
#         statename = re.search('https://www.usclimatedata.com/climate/(.+?)/united-states', line).group(1)
#         statename = statename.title()
#         statename = statename.replace('-', ' ')
#         states[statename] = line.strip()
# states.append(line.strip())
# print(states)

# for state part print(states.split("/")) then split on -, just in case. Then Title.
# print(weather.content)
# print(type(w))
# w = """var the_data = \'[{"Month": "Jan", "Low":36, "High":57, "Precipitation": 4.65},{"Month": "Feb", "Low":39, "High":62, "Precipitation": 5.28},{"Month": "Mar", "Low":45, "High":70, "Precipitation": 5.94},{"Month": "Apr", "Low":52, "High":77, "Precipitation": 4.02},{"Month": "May", "Low":61, "High":84, "Precipitation": 3.54},{"Month": "Jun", "Low":68, "High":90, "Precipitation": 4.06},{"Month": "Jul", "Low":71, "High":92, "Precipitation": 5.24},{"Month": "Aug", "Low":71, "High":92, "Precipitation": 3.98},{"Month": "Sep", "Low":65, "High":87, "Precipitation": 3.98},{"Month": "Oct", "Low":53, "High":78, "Precipitation": 2.91},{"Month": "Nov", "Low":44, "High":69, "Precipitation": 4.61},{"Month": "Dec", "Low":37, "High":60, "Precipitation": 4.84}]\';\t\t\n\tvar precipitation_max """

# state_wthr = {}

# error = 0
# for key, value in states.items():
#     weather = requests.get(value)
#     w = weather.content.decode()
#     try:
#         found = re.search('var the_data = \'(.+?)\';\t\t\n\tvar precipitation_max', w).group(1)
#         state_wthr[key] = found
#     except AttributeError:
#         found = ''  # apply your error handling
#         error += 1
#     print(found)

# print(error)
# print(state_wthr)

state_wthr = {}
with open("statesweather.txt") as f:
    state_wthr = eval(f.readline())
# print(state_wthr)
with open("stateweathervals.txt", "w+") as f:
    for key, val in state_wthr.items():
        evOct = eval(state_wthr[key])[9]
        evNov = eval(state_wthr[key])[10]
        octAvg = (evOct["Low"] + evOct["High"]) / 2
        novAvg = (evNov["Low"] + evNov["High"]) / 2
        stateAvg = (octAvg + novAvg) / 2
        f.write(key + ": " + str(ceil(stateAvg)) + "\n")
