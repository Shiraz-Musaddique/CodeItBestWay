#!/bin/bash
for i in `cat Upper-ALL`
do
sshpass ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no -t autouser@$i "echo "========" ; sudo hostname -i ; uname -r ; cat /etc/redhat-release ; echo "=======" " | tee -a Upper-Kernel-Version-$(date +%m-%d-%Y).log
done

#paste all your IP addresses in this file Upper-ALL. MAke sure that both the file and script should be in same directory.
#####################################################
#Below is the output of above script                #
#========                                           #  
#10.165.224.190                                     #
#3.10.0-1127.el7.x86_64                             #
#Red Hat Enterprise Linux Server release 7.8 (Maipo)#
#=======                                            #
#####################################################