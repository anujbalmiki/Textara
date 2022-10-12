import json
import urllib.request
from http.client import HTTPResponse
from urllib import response
from docx import Document
from django.http import HttpResponseNotModified, FileResponse
from django.shortcuts import redirect, render

from .models import users, contact_form
from home_app.models import user_activity
from django.contrib.auth.models import User, auth
from django.contrib import messages
from fpdf import FPDF
import pathlib
import os

# for sending the mail
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Create your views here.


def user_dashboard_view(request, *args, **kwargs):
    if request.user == "AnonymousUser":
        return redirect('login')
    else:
        activity = user_activity.objects.filter(user_name=request.user)
        return render(request, 'user_dashboard.html', {'user_activity': activity, 'username': request.user})


def login_view(request, *args, **kwargs):
    return render(request, 'login.html', {})


def register_view(request, *args, **kwargs):
    return render(request, 'register.html')


def register1(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username_field']
        email = request.POST['email_field']
        password = request.POST['password_field']
        cnf_password = request.POST['cnf_password_field']
        tandc = request.POST['remeberme_checkbox']

        if password == cnf_password:
            if User.objects.filter(username=username).exists():
                messages.warning(request,
                                 "This Username is already taken, please choose another.")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.warning(request,
                                 "A user with this email already exixts, please use another email or go to login")
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                user.save()
                send_mail(email, username, password, first_name, last_name)

                return redirect("login")
        else:
            messages.warning(request, "Two password fields shoulb be matching")
            return redirect('register')

    else:
        return render(request, 'register.html')


def send_mail(email, username, password, first_name, last_name):
    sender_email = "textarateam@gmail.com"
    receiver_email = email
    sender_password = "neszwjcjwvlsbfuw"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Greetings from the Textara Team"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hi, """+first_name+""" """+last_name+"""
    Welcome to Textara, the best text recognizer on the web.
    We are glad to have you on board.
    Your username and password are as follows:
    """+username+"""
    """+password+""""""
    html = """\
    <html>
    <body>
        <h1>Hi, """+first_name+""" """+last_name+"""</h1><br>
        <h3>Welcome to Textara, the best text recognizer on the web.<br>
        We are glad to have you on board.<br>
        Your username and password are as follows:<br>
        """+username+"""<br>
        """+password+"""<br>
        </h3><br>
    </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, sender_password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


def login(request):
    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']
        remember_me = request.POST.getlist('rememberme_checkbox')
        print("Reemember me is: ", remember_me)

        user = auth.authenticate(request, username=email, password=password)

        if user is not None:
            auth.login(request, user)
            if remember_me != ['true']:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600)
            return redirect("your_activities")
        else:
            messages.info(
                request, "Please enter correct credentials or register")
            return redirect("login")

    else:
        return render(request, 'login.html')


def logout(request, *args, **kwargs):
    auth.logout(request)
    return redirect('/')


def delete_activity(request, id):
    activity = user_activity.objects.get(id=id)
    activity.delete()
    return redirect(user_dashboard_view)


def save_as_doc(request, text, id):
    text_to_save = text
    text_id = id
    return render(request, 'save_as_doc.html', {'text': text_to_save, 'id': text_id})


def save_as_pdf(request, text, id):
    save_this_text = text
    text_id = id

    # dir = os.path.join(settings.MEDIA_ROOT, self.docfile.name)
    # for f in os.listdir(dir):
    #     os.remove(os.path.join(dir, f))

    path = 'media/YourFile'+text_id+'.pdf'

    save_this_text.encode('raw-unicode-escape').decode('utf-8')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=save_this_text, align='L')
    pdf.output(path)

    response = FileResponse(open(path, 'rb'))

    return response


def save_as_txt(request, text, id):
    save_this_text = text
    text_id = id

    # dir = os.path.join(settings.MEDIA_ROOT, self.docfile.name)
    # for f in os.listdir(dir):
    #     os.remove(os.path.join(dir, f))

    path = 'media/YourFile'+text_id+'.txt'

    text_file = open(path, 'w', encoding='utf-8')
    text_file.write(save_this_text)
    text_file.close()

    response = FileResponse(open(path, 'rb'))

    return response


def save_as_word(request, text, id):
    save_this_text = text
    text_id = id

    # dir = os.path.join(settings.MEDIA_ROOT, self.docfile.name)
    # for f in os.listdir(dir):
    #     os.remove(os.path.join(dir, f))

    path = 'media/YourFile'+text_id+'.docx'

    document = Document()
    document.add_paragraph(save_this_text)
    document.save(path)

    response = FileResponse(open(path, 'rb'))

    return response


# accepting the contact form
def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        contact = contact_form(name=name, email=email,
                               subject=subject, message=message)
        contact.save()

        messages.success(
            request, "Thank you for contacting us.We will get back to you soon.")
        print("Contact form submitted")
        return redirect('contact')
    else:
        return render(request, 'contact.html')
