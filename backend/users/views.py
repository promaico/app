from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import RegistrationForm,LoginForm, Email_Form #ProfileForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.urls import reverse
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.decorators import login_required
from imapclient import IMAPClient
import logging
import ssl
import quopri
from dotenv import load_dotenv
import os


# Create your views here.
def index(request):
    messages_to_display = messages.get_messages(request)
    return render(request, 'users/index.html', {"messages": messages_to_display})

def RegistrationView(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User = form.save(commit= False)
            User.is_active = False
            User.save()
            
            current_site = get_current_site(request)
            mail_subject = "Aktivieren sie ihr Konto"
            message = render_to_string("registration/account_activation_email.html", {
                "user": User,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(User.pk)),
                "token": account_activation_token.make_token(User)
            })
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, "Bitte prüfen Sie Ihre E-Mail, um die Registrierung abzuschließen.")
            return redirect("index")
    return render(request, "registration/register.html", {"form": form})

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Ihr Account wurde erfolgreich aktiviert!")
        return redirect(reverse("login"))
    else:
        messages.error(request, "Ihr Link zur Aktiviertung ist entweder ungültig oder abgelaufen!")
        return redirect("index")


def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                form = LoginForm()
                login(request, user)
                if request.user.is_authenticated():
                    messages.success(request, "Sie haben sich erfolgreich eingeloggt!")  # Display login success message
                    return redirect("profile")
                else:
                    messages.error(request, "Fehler beim Einloggen. Bitte überprüfen Sie Ihre Anmeldeinformationen.")  # Display login error message
    return render(request, "registration/login.html", {"form": form})

def email_view(request):
    MAILSEARCH = request.GET["sender"]
    host = 'imap.gmail.com'
    user =  'tjark.jakob.de@gmail.com'
    password =  "sfwu cbae cfqy tjoj"

    FOLDER = "INBOX"

    context1 = []

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s: %(message)s',
        level=logging.INFO
    )

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        with IMAPClient(host, ssl_context=ssl_context) as server:
            server.login(user, password)
            select_info = server.select_folder(FOLDER)


            messages = server.search(['FROM', MAILSEARCH])


            for msgid, data in server.fetch(messages, ['ENVELOPE']).items():
                envelope = data[b'ENVELOPE']
                
                #add info to list
                
                msgid = {
                    "id": msgid,
                    "Datum": envelope.date,
                    "Betreff": envelope.subject.decode(),
                }
                
                context1.append(msgid)
                
                
            # Nachrichten abrufen (inklusive BODY[TEXT])
            response = server.fetch(messages, ['BODY[TEXT]'])

            # Nachrichten durchgehen und anzeigen
            for msgid, data in response.items():
                # Entschlüssle den Text aus den Bytes
                decoded_text = quopri.decodestring(data[b'BODY[TEXT]']).decode('utf-8')

                # Zeige den entschlüsselten Text an
                for dict in context1:
                    if dict.get("id") == msgid:
                        dict["Inhalt"] = decoded_text
                        
                    

            context = {
                'emails': context1
            }
            
            print(context)
            

    except Exception as e:
        print(f"Error: {e}")

    
    #return render(request,  context)
    return render(request, "users/profile_email.html", context)

def profile_view(request):
    return render(request, 'users/profile.html')


