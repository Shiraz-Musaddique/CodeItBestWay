#!/bin/bash

for REGION in $(aws ec2 describe-regions --output text --query 'Regions[].[RegionName]') ;

do

  echo $REGION && aws ec2 describe-volumes --filter "Name=status,Values=available" --query 'Volumes[*].{VolumeID:VolumeId,Size:Size,Type:VolumeType,AvailabilityZone:AvailabilityZone}' --region $REGION;

done
