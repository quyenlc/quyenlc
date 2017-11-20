#!/usr/bin/python
import sys
import boto3
from pprint import pprint
client = boto3.client(
    'ec2',
    aws_access_key_id='AKIAJM4KYHN5INWP34UA',
    aws_secret_access_key='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',
    region_name='us-west-1'
)
avolumes = client.describe_volumes()
ainstance = client.describe_instances()

def get_volume_info(volume_id):
    for volume in avolumes['Volumes']:
        if (volume['VolumeId'] == volume_id):
            print "ID: {}".format(volume['VolumeId'])
            print "Type: {}".format(volume['VolumeType'])
            print "Size: {}".format(volume['Size'])
            if ('standard' != volume['VolumeType']):
                print "IOPS: {}".format(volume['Iops'])


for instance in ainstance['Reservations']:
    instance_info = instance['Instances'][0]
    for tag in instance_info['Tags']:
        if (tag['Key'] == 'Name'):
            if (str(tag['Value'].find('ult-n-db')) != '-1'):
                print "Instance Name: {}".format(tag['Value'])
                for device in instance_info['BlockDeviceMappings']:
                    if (str(device['DeviceName'].find('/dev/sda'))=='-1'):
                        print "DeviceName: {}".format(device['DeviceName'])
                        get_volume_info(device['Ebs']['VolumeId'])
