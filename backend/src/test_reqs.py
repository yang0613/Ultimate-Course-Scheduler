#!/usr/bin/python3
import json
import reqs

json_file = open("dummy_schedule.json")
schedule = json.load(json_file)
txt_file = open("CSEMajorDeclare.txt", "r")
declare_major = txt_file.read()
txt_file.close()
json_file.close()

req = reqs.requirement(declare_major)
print(req.validate(schedule))
