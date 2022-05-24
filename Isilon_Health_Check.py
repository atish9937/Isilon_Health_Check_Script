import paramiko,os,re,HTML,smtplib,time,base64
def get():
    cd=os.getcwd()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s=open("Isilon_Cred.txt","r")
    table_content=[]
    for i in s.readlines():
        rows=[]
        i=i.strip().split(",")
        rows.append("<strong>{}</strong>".format(i[0]))
        u=base64.b64decode(i[2])
        p=base64.b64decode(i[3])
        try:
            ssh.connect(i[1], username=u, password=p)
            stdin, stdout, stderr = ssh.exec_command("isi status")        
            opt=''.join(stdout.readlines())
            with open("tmp.txt","w") as f:   
                f.write(opt)
            with open("tmp.txt","r") as f:
                isilon_issue=[]
                for line in f.readlines():       
                    line=line.strip()
                    line=re.sub("[ \t\n]+"," ",line)
                    if re.search("Cluster Health:",line):
                        if "OK" not in line:
                            rows.append(line)
                        else:
                            rows.append("OK")
        except Exception as err:
                rows.append("<p style='background-color:red'>{}</p>".format(err))
        table_content.append(rows)
    s.close()
    return table_content
def get_html(table_data):
    header=['Cluster Name',"Health Status"]
    htmlcode = HTML.table(table_data,header_row=header)
    with open("htmlfile.html","w") as f:
        f.write(htmlcode)
    fhtml=open("fhtml.html","w")
    with open("htmlfile.html","r") as f:
        fhtml.write(open("html_body.html").read())
        for line in f.readlines():
            if "<TD><TABLE" in line:
                line=line.replace("<TD><TABLE","<TD valign='top'><TABLE")
                fhtml.write(line)
            elif "OK" in line:
                line=line.replace("<TD>","<TD style='background-color:#00ff00'>")
                fhtml.write(line)
            elif "Cluster Health:" in line:
                line=line.replace("<TD>","<TD style='background-color:red'>")
                fhtml.write(line)
            else:
                fhtml.write(line)
        fhtml.write("{} </body>".format(time.ctime()))
    fhtml.close()
    html_table=open("fhtml.html","r").read()
    return html_table
def mail(html_table_code):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    From = "fromemail@xyz.com"
    To = ["email1@xyz.com","email2@xyz.com"]
    Cc = ["email3@xyz.com","email4@xyz.com"]
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Isilon Health Status Report"
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
    s = smtplib.SMTP("smtpserver.xyz.com",25)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    #s.sendmail(From, To + Cc, msg.as_string())
    s.sendmail(From, To + Cc , msg.as_string())
    s.quit()
data=get()    
html_table_code=get_html(data)
mail(html_table_code)

