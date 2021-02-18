#!/bin/python
import boto3
import datetime
TODAY=datetime.datetime.now()
OutputFile="/local/apps/infra/reports/inventory/AWS_EC2_INV_NonProd.csv"
InstReport=open(OutputFile,'w')
InstReport.write("VPC ID,Instance ID,Instance Name,IP Addr,Instance Type,State,Instance Owner,ServerRole,Availability Zone,Environment,Datadog,AppID,Platform,CPU Cores,Threads per Core,Total vCPU,Instance Profile,Creation Date,Age(Days),EMR Cluster ID,EMR Node,Today\n")
for REGION in ['us-east-1','us-west-2']:
    boto3.setup_default_session(region_name=REGION)
    client = boto3.client('ec2')
    response = client.describe_instances()
    for RESP in response['Reservations']:
        for INST in RESP['Instances']:
            #print INST
            STATE=INST['State']['Name']
            if STATE == "terminated" or STATE == "shutting-down":
                continue
            INSID=INST['InstanceId']
            IP=INST['PrivateIpAddress']
            VPCID=INST['VpcId']
            AZ=INST['Placement']['AvailabilityZone']
            try:
                INSTPROF=INST['IamInstanceProfile']['Arn'].split(":")[5].split('/')[1]
            except KeyError:
                INSTPROF=""
            try:
                INSTCRDT=str(INST['NetworkInterfaces'][0]['Attachment']['AttachTime']).split(" ")[0]
                #print INSTCRDT
            except KeyError:
                INSTCRDT=""
            TYPE=INST['InstanceType']
            try:
                PLATFORM=INST['Platform']
            except KeyError:
                PLATFORM="-"
            CORES=INST['CpuOptions']['CoreCount']
            TPC=INST['CpuOptions']['ThreadsPerCore']
            VCPU=CORES * TPC
            InstanceOwner=""
            InstanceName=""
            InstanceRole=""
            InstanceENV=""
            InstanceAppID=""
            DataDog=""
            BuildDate=INSID
            AGE=""
            EMRNode=""
            EMRCluserID=""
            #print INST
            if 'Tags' in INST:
                for tags in INST['Tags']:
                    if tags["Key"] == 'Name':
                        InstanceName = tags["Value"]
                    elif tags["Key"] == 'Owner':
                        InstanceOwner = tags["Value"]
                    elif tags["Key"] == 'ServerRole':
                        InstanceRole = tags["Value"]
                    elif tags["Key"] == 'Environment':
                        InstanceENV = tags["Value"]
                    elif tags["Key"] == 'AppID':
                        InstanceAppID = tags["Value"]
                    elif tags["Key"] == 'Datadog':
                        DataDog = tags["Value"]
                    elif tags["Key"] == 'BuildDate':
                        BuildDate = tags["Value"]
                    elif tags["Key"] == 'aws:elasticmapreduce:instance-group-role':
                        EMRNode = tags["Value"]
                    elif tags["Key"] == 'aws:elasticmapreduce:job-flow-id':
                        EMRCluserID = tags["Value"]
            if BuildDate == INSID:
                print "Entered Createdate"
                client.create_tags(
                        Resources=[INSID],
                        Tags=[
                        {
                            'Key': 'BuildDate',
                            'Value': INSTCRDT
                        },
                        ]
                        )
            PYCRDT=datetime.datetime(int(INSTCRDT.split('-')[0]), int(INSTCRDT.split('-')[1]), int(INSTCRDT.split('-')[2]))
            AGE=(TODAY - PYCRDT).days
            if AGE >= 330:
                client.create_tags(
                        Resources=[INSID],
                        Tags=[
                        {
                            'Key': 'OldAMI',
                            'Value': 'Yes'
                        },
                        ]
                        )
            else:
                client.create_tags(
                        Resources=[INSID],
                        Tags=[
                        {
                            'Key': 'OldAMI',
                            'Value': 'No'
                        },
                        ]
                        )



            #print ("{0},{1},{2},{3},{4},{5},{6},{7}".format(VPCID,INSID,InstanceName,IP,STATE,InstanceOwner,InstanceRole,AZ))
            InstReport.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19},{20},{21}\n".format(VPCID,INSID,InstanceName,IP,TYPE,STATE,InstanceOwner,InstanceRole,AZ,InstanceENV,DataDog,InstanceAppID,PLATFORM,CORES,TPC,VCPU,INSTPROF,INSTCRDT,AGE,EMRCluserID,EMRNode,TODAY))
~
