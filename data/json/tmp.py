import json
import random
from datetime import datetime as dt

groups = {
    1: [1, 2, 9],
    2: [3, 15, 7],
    3: [4, 7, 6],
    4: [15, 10],
    5: [12, 14, 4],
    6: [5, 11],
    7: [12, 3, 6, 5],
    8: [5, 10, 8],
    9: [6, 7],
    10: [9, 10, 8, 7],
    11: [6, 13, 9]
}
with open("dates.json", "r") as file:
    dates = json.load(file)
attendances = []

for date_num in range(len(dates)):
    for group in groups:
        if group != dates[date_num]['gid']:
            continue
        for student in groups[group]:
            
            status = bool(random.randint(0, 5)) if dt.strptime(dates[date_num]['date'], '%Y-%m-%d') <= dt(2021, 6, 21) else False
            
            attendances.append({
                "did": date_num + 1,
                "status": status,
                "sid": student,
            })

with open('attendances.json', 'w') as file:
    json.dump(attendances, file, indent=4)

