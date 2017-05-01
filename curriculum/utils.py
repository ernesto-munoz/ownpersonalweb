import smtplib
from email.mime.text import MIMEText


class SendMail(object):

    @staticmethod
    def send_mail(sender, to, subject, message):
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = 'emunozfaba@gmail.com'

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.ehlo_or_helo_if_needed()

        try:
            failed = server.sendmail(sender, to, msg.as_string())
            server.close()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    SendMail.send_mail('hola@gmail.com', 'emunozfaba@gmail.com', "Super", "bien")