# Isilon_Health_Check_Script
A simple EMC Isilon health check script written in Python

Step 1. Install Python and required libraries. HTML library can be downloaded from https://www.decalage.info/python/html.

Step 2. Create a "Isilon_Cred.txt" file and mention the cluster that you want to monitor. Make sure to keep the credential file and script file in same folder.

  Format would be: clustername,username,password
  
  Make sure that user name and password should be base64 encoded you can encode username and password from https://techieblogging.com/base64-encode-and-decode-string/
  
  for example if username is "root" and the password for the cluster are "password", then the Isilon_Cred.txt should look like below
  
  cluster1,"cm9vdA==","cGFzc3dvcmQ="
  
  cluster2,"cm9vdA==","cGFzc3dvcmQ="
  
Step 3. Modify the script file as per your environment.

  For example you should modify, from address,cc, to address, Subject line, and smtp server address.
  
Step 4. Schedule the script on crontab or in windows schedular. You can also run it manually. Just go to folder by CMD and type "python scriptname.py"
