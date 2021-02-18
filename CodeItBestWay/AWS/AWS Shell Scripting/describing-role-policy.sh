#!/bin/bash
#This script will give provide you the policies attached to the role and also their permissions.
#This script needs aws-cli v2 installed mandatory in the system
# you need to run this script 2 times everytime  they have to provide role name. it will create one file with policy and second time run you have to redirect the output to the file.


read -p "Please Enter AWS ROLE Name and see the game: " rolename
FILE=$rolename-policies

if [ ! -f $FILE ]; then

role=$(/usr/local/bin/aws2 iam list-attached-role-policies --role-name $rolename --output yaml | awk 'NR % 2 == 0' | awk '{ $1=""; $2=""; print}')
echo "$role" >> $FILE
echo "Please run the script again like this: sh policy.sh >> output"
else
#echo "do nothing"
#cat $FILE
for i in `cat $FILE`
do
out=$(/usr/local/bin/aws2 iam get-policy --policy-arn $i | grep -i "DefaultVersionId" | awk 'NR==1{print $2}' | sed 's/[\"\,]//gi')
policy=$(echo $i | awk -F ":" '{print $6}')
echo "===================Start Policy================="
echo "PolicyName: $policy"
echo "DefaultVersionId for the policy: $out"
/usr/local/bin/aws2 iam get-policy-version --policy-arn $i --version-id "$out" --output yaml
echo "========================END====================="
done
fi
