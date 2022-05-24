import paramiko,os,re,HTML,smtplib,time,base64
def get():
    cd=os.getcwd()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s=open("Unity_Cred.txt","r")
    table_content=[]
    for i in s.readlines():
        rows=[]
        i=i.strip().split(",")
        rows.append("<strong>{}</strong>".format(i[0]))
        u=base64.b64decode(i[2]).decode("utf-8")
        p=base64.b64decode(i[3]).decode("utf-8")
        try:
            ssh.connect(i[1],username="service",password=p)
            cmd="uemcli -d {} -u Local/{} -p {} /sys/general show -detail".format(i[1],u,p)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            stdin.write("1\n")
            opt=''.join(stdout.readlines())
            with open("tmp.txt","w") as f:   
                f.write(opt)
            with open("tmp.txt","r") as f:
                health_issue=[]
                for line in f.readlines():       
                    line=line.strip()
                    line=re.sub("[ \t\n]+"," ",line)
                    if re.search("Product serial number",line):
                        rows.append(line.split("=")[-1])
                    elif re.search("Health details",line):
                        line=line.split("=")
                        if "The system is operating normally." in line[1]:
                            rows.append(line[1])
                        else:
                            rows.append(line[1])
        except Exception as err:
                rows.append("NA")
                rows.append("<p style='background-color:red'>{}</p>".format(err))
        table_content.append(rows)
    s.close()
    return table_content
def get_html(table_data):
    cd=os.getcwd()
    ####Start HTML Table For Inode Increase Count####
    header=["Unity Name","Serial Number","Status"]
    htmlcode = HTML.table(table_data,header_row=header)
    #print(htmlcode)
    with open("htmlfile.html","w") as f:
        f.write(htmlcode)
    fhtml=open("Unity.html","w")
    with open("htmlfile.html","r") as f:
        fhtml.write(open("html_body.html").read())
        for line in f.readlines():
            if "The system is operating normally." in line:
                line=line.replace("<TD>","<TD style='background-color:#00ff00'>")
                fhtml.write(line)
            else:
                fhtml.write(line)
        fhtml.write("</body>")
    fhtml.write("<br>{}".format(time.ctime()))
    fhtml.close()
    html_table=open("Unity.html","r").read()
    return html_table
def mail(html_table_code):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    From = "fromemailaddress@xyz.com"
    To = ["toemailaddress1@xyz.com","toemailaddress2@xyz.com"]
    Cc = ["ccemailaddress1@xyz.com","ccemailaddress2@xyz.com",]
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Unity Health Check Report"
    msg['From'] = From
    msg['To'] = ",".join(To)
    msg['Cc'] = ",".join(Cc)
    # Create the body of the message (a plain-text and an HTML version).
    # Record the MIME types of both parts - text/plain and text/html.
    #part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html_table_code, 'html')
    # Attach parts into message container.
    msg.attach(part2)
    # Send the message via local SMTP server.
    s = smtplib.SMTP("smtpserver@xyz.com",25)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(From, To + Cc, msg.as_string())
    s.quit()
data=get()    
html_table_code=get_html(data)
#mail(html_table_code)

