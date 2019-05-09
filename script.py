# -*- coding: utf-8 -*-
"""
Created on Wed May  8 18:57:37 2019

@author: AhmadBilal
"""

import boto3
import pandas as pd
import json

account = input("Insert account name: ")
boto3.setup_default_session(profile_name=account)


ec2 = boto3.client('ec2')

custom_filter = [{'Name':'tag:cloudhesivemanaged',
                  'Values':['true']}]

response = ec2.describe_instances(Filters = custom_filter)
response = response['Reservations']

list = []
for i in response:
    for p in i['Instances']:
        month = str(p['LaunchTime'].month)
        day = str(p['LaunchTime'].day)
        year = str(p['LaunchTime'].year)
        date = month+"-"+day+"-"+year
        list.append([p['InstanceId'],date])


df = pd.DataFrame(list, columns = ['instance_id', 'launch_time'])


with open("datadog.json") as file:
    jsondata = json.load(file)
    
datadog_list = df['instance_id'].tolist()
datadog_not_installed = []

for host in jsondata['rows']:
    if str(host['display_name']) in datadog_list and ('agent' not in host['apps']):
        datadog_not_installed.append(host['display_name'])

s = df['instance_id']
df['datadog_installed'] = s.isin(datadog_not_installed)

print(df)