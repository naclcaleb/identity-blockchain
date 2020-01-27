import datetime
import json

def datetime_from_iso(dt_str):
        dt, _, us= dt_str.partition(".")
        dt= datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
        us= int(us.rstrip("Z"), 10)
        return dt + datetime.timedelta(microseconds=us)

def json_from_file(filename):
    json_obj = None
    with open(filename, 'r') as file:
        json_str = file.read()
        json_obj = json.loads(json_str)
    return json_obj