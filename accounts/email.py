from django.conf import settings
from django.core.mail import EmailMessage



# EMAIL OTP TEMPLATE  -  FINFLO TESTING ENV


def email_to(to_email,key):
    
    subject = "OTP for Finflo Login "

    message = """
        Dear {0},
        your otp to login in finflo is {1} .
        if any support needed contact support@finflo.com
    """.format(str(to_email),str(key))

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [to_email]
    cc_list = ["anand98.ar@gmail.com"]

    email = EmailMessage(
        subject,
        message,
        email_from,
        recipient_list,
        cc_list,
    )
    email.send(fail_silently=False)