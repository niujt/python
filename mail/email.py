import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = 'smtp.163.com'
receiver = ['670482466@qq.com']
message = MIMEText('发送测试报告!!!', 'plain', 'utf-8')
message['from'] = Header('张伟', 'utf-8')
message['To'] = Header('钮佳涛', 'utf-8')

subject = 'PYTHON 邮件测试'
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP()
    smtpObj.sendmail(sender, receiver, message.as_string())
    print('send success')
except smtplib.SMTPException as e:
    print(e)
    print('error f**k!!!')
