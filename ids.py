import csv
# Fullname : UserId

nameToID = {}
idToName = {}
with open('csvs/ids.csv') as f:
    reader = csv.reader(f)
    next(reader)
    nameToID = {rows[0]: rows[1] for rows in reader}
    idToName = {rows[1]: rows[0] for rows in reader}
keys = list(nameToID.keys())
