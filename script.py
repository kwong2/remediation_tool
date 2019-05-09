# -*- coding: utf-8 -*-
"""
Created on Wed May  8 18:57:37 2019

@author: AhmadBilal
"""

#Import packages
import boto3
import pandas as pd
import json

#Switch to appropriate role/account
account = input("Insert account name: ")
boto3.setup_default_session(profile_name=account)

#Initiate ec2 session
#Create filter for instances with cloudhesivemanaged tag = true 
#Import using describe_instances
ec2 = boto3.client('ec2')
custom_filter = [{'Name':'tag:cloudhesivemanaged',
                  'Values':['true']}]
response = ec2.describe_instances(Filters = custom_filter)

#Parse response object, extract InstanceID & launch date, append to list
list = []
response = response['Reservations']
for i in response:
    for p in i['Instances']:
        month = str(p['LaunchTime'].month)
        day = str(p['LaunchTime'].day)
        year = str(p['LaunchTime'].year)
        date = month+"-"+day+"-"+year
        list.append([p['InstanceId'],date])


#Create dataframe
df = pd.DataFrame(list, columns = ['instance_id', 'launch_time'])

#Import datadog json data
with open("datadog.json") as file:
    jsondata = json.load(file)
    
#Capture InstanceID's that don't have datadog agent, add column to dataframe
datadog_list = df['instance_id'].tolist()
datadog_not_installed = []
for host in jsondata['rows']:
    if str(host['display_name']) in datadog_list and ('agent' not in host['apps']):
        datadog_not_installed.append(host['display_name'])
s = df['instance_id']
df['datadog_installed'] = s.isin(datadog_not_installed)

print(df)