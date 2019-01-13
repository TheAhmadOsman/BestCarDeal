import csv
import random
with open('craigslistVehiclesFull.csv', 'r') as inp, open('craigslistVehiclesReduced.csv', 'w') as out:
    writer = csv.writer(out)
    first = False
    for row in csv.reader(inp):
        foo = random.randint(1, 10)
        if foo == 1 or first == False:
            writer.writerow(row)
            first = True