#!/usr/bin/python
import sys
import boto3
from datetime import datetime, timedelta
one_minutes_ago = datetime.utcnow() - timedelta(minutes=1);
six_minutes_ago = datetime.utcnow() - timedelta(minutes=6);
cache_cluster_id = sys.argv[1];
metric_name = sys.argv[2];
statistic = 'Average';
if len(sys.argv) >= 4:
    statistic= sys.argv[3];
client = boto3.client(
    'cloudwatch',
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name='us-west-1'
)
response = client.get_metric_statistics(
    Namespace='AWS/ElastiCache',
    MetricName=metric_name,
    StartTime=six_minutes_ago , # Change it
    EndTime=one_minutes_ago,
    Period=300,
    Statistics=[statistic],
    Dimensions=[
        {
            'Name': 'CacheClusterId',
            'Value': cache_cluster_id
        }
    ] 
);
datapoints = response.get('Datapoints');
datapoint = datapoints[0];
print(datapoint.get('Average'));