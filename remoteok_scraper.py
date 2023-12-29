import requests
import xlwt
from xlwt import Workbook
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

BASE_URL = "https://remoteok.com/api"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0" #I get that from whatismybrowser.com just seach for user agent
REQUEST_HEADER = {
    "User-Agent" : USER_AGENT,
    'Accept-Language' : "en-US, en;q=0.5",
}

def get_posting_jobs():
    return requests.get(url = BASE_URL, headers = REQUEST_HEADER).json()

def output_jobs_to_xls(data):
    wb = Workbook()
    job_sheet = wb.add_sheet('Jobs')
    headers = list(data[0].keys())

    # writing header values on xls it's like thead 
    for i in range(0, len(headers)):
        job_sheet.write(0,i,headers[i])
    
    # writing data on xls its like tbody
    for i in range(0, len(data)):
        job = data[0]
        values = list(job.values())
        for j in range(0, len(values)):
            job_sheet.write(i+1, j, values[j])

    # save xls file
    wb.save('remote_jobs.xls')

def send_email(send_from, to, subject, text, files=None):
    assert isinstance(to, list)
    msg = MIMEMultipart()
    msg["From"] = send_from
    msg["To"] = COMMASPACE.join(to)
    msg["Date"] = formatdate(localtime = True)
    msg["Subject"] = subject

    msg.attach(MIMEText(text))

    for file in files or []:
        with open(file, "rb") as f:
            part = MIMEApplication(f.read(), Name=basename(file))
        part["Content-Disposition"] = f'attachment; filename = "{basename(file)}"'
        msg.attach(part)

    smtp = smtplib.SMTP('smtp.gmail.com', '587')
    smtp.starttls()
    smtp.login(send_from, 'vtte efnx ydgk ezyc')
    smtp.sendmail(send_from, to, msg.as_string())
    smtp.close()


if (__name__ == "__main__"):
    # print(get_posting_jobs()[1:])
    # output_jobs_to_xls(get_posting_jobs()[1:])
    send_email('prgaming.ismail@gmail.com', ['prgaming.ismail@gmail.com'], 'Jobs posting', 'msg', files = ['remote_jobs.xls'])