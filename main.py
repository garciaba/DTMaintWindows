import os, requests, time, sched, random, json, csv, re, math
import msvcrt as m
from datetime import datetime, timedelta


# Function for waiting for key press
def wait():
    m.getch()


def parsear_hosts():
    f = open('data/HostJsonData.json')
    data = json.load(f)

    with open('data/TargetHostsRefactored.csv', "w+", newline='') as myfile:
        writerfile = csv.writer(myfile, delimiter=';')
        writerfile.writerow(["Entity", "ID"])
        for k in data:
            host = k["discoveredName"].split(".", 1)
            writerfile.writerow([host[0], k["entityId"]])


def comparar_hosts(YOUR_DT_API_URL, YOUR_DT_API_TOKEN):
    with open('data/TargetHostsRefactored.csv', "r") as comp1, open('data/maintenance_calendar_SAN.csv', 'r') as comp2:

        csv_reader = csv.DictReader(comp1, delimiter=";")
        csv_reader2 = csv.DictReader(comp2, delimiter=";")

        for row in csv_reader:
            print(row["Entity"] + ": " + row["ID"])
            for row2 in csv_reader2:
                print(row2['ROBOT'] + " compara con " + row["Entity"])
                if row2['ROBOT'].casefold() == row["Entity"].casefold():
                    print(row2['ROBOT'] + " es igual a " + row["Entity"])
                    hostID = row["ID"]
                    timeToSplit = row2['TIME_BEGIN_MAINTENANCE'].split(":", 1)
                    print(timeToSplit[1])  # seleccionar YY
                    YY = (int(timeToSplit[1])) - int(timeToSplit[1]) % 15
                    XX = timeToSplit[0]
                    if len(str(YY)) == 1: YY = "0" + str(YY)
                    if len(str(XX)) == 1: XX = "0" + str(XX)
                    finalTag = str(XX) + str(YY)
                    print(finalTag)
                    tagear_host(YOUR_DT_API_URL, YOUR_DT_API_TOKEN, finalTag, hostID)
            comp2.seek(0)  # reiniciar DictReader


def tagear_host(YOUR_DT_API_URL, YOUR_DT_API_TOKEN, finalTag, hostID):

    headers = {'Content-Type': 'application/json', 'Authorization': 'Api-Token ' + '_'.join(YOUR_DT_API_TOKEN)};
    url = ''.join(YOUR_DT_API_URL) + '/api/v1/entity/infrastructure/hosts/' + ''.join(hostID);
    tag = "MaintWindow:" + finalTag
    body = {"tags": ["MaintWindow:" + finalTag]}
    print(body)
    response = requests.post(url, data=body, headers=headers)

def get_total_hosts(YOUR_DT_API_URL, YOUR_DT_API_TOKEN):
    r = requests.get(
        ''.join(YOUR_DT_API_URL) + '/api/v1/entity/infrastructure/hosts?includeDetails=false&Api-Token=' + ''.join(
            YOUR_DT_API_TOKEN) + '&pageSize=5000&relativeTime=day&showMonitoringCandidates=false');
    json_data = r.json()
    json_formatted_str = json.dumps(json_data, indent=2)
    f = open("data/HostJsonData.json", "w")
    f.write(json_formatted_str)


with open('data/credenciales.csv') as csv_file:
    # read the input file
    csv_reader = csv.reader(csv_file, delimiter=',')
    # get the URL and the token from the input file
    YOUR_DT_API_URL = next(csv_reader)
    YOUR_DT_API_TOKEN = next(csv_reader)

print("    Environment: ", YOUR_DT_API_URL)

get_total_hosts(YOUR_DT_API_URL, YOUR_DT_API_TOKEN)
parsear_hosts()
comparar_hosts(YOUR_DT_API_URL, YOUR_DT_API_TOKEN)
