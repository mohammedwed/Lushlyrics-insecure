from django.db import IntegrityError
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import playlist_user, UserOTP
from django.urls.base import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from youtube_search import YoutubeSearch
import json
import random
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse
import logging

# import cardupdate


f = open("card.json", "r")
CONTAINER = json.load(f)


# I know this is not a good practise
def generate_otp():
    """Generates a 6-digit integer OTP."""
    otp = random.randint(100000, 999999)
    return str(otp)


def default(request):
    if request.user.is_authenticated:
        song = "kSFJGEHDCrQ"
        return render(request, "player.html")
    # else:
    return redirect('user_login_handler')
    # if request.method=="POST":
  
def user_logout_handler(request):
    logout(request)
    return redirect('user_login_handler')
          
def user_login_handler(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username)
        print(password)

        # Authenticate user
        print("Before auth user")
        user = authenticate(request=request, username=username, password=password)
        print("After auth user")

        if user is not None:
            # User is authenticated, log them in
            login(request, user)
            # Redirect to a successful login page (e.g., profile page)
            print("Login Suecess")
            return redirect('default')
        else:
            # Invalid login credentials
            print("Invalid username or password")
            # Display an error message on the login page
            return render(
                request, "login.html", {"case": "Invalid username or password"}
            )


def user_registration_handler(request):
    if request.method == "GET":
        return render(request, "signup.html")
    elif request.method == "POST":
        # Retrieve form data
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        #confirm_password = request.POST.get("confirm-password")

        # if password != confirm_password:
        #     print("Error: Passwords don't match")
        #     return render(request, "signup.html")

        username_exists = User.objects.filter(username=username).exists()
        email_exists = User.objects.filter(email=email).exists()

        try:
            if username_exists and email_exists:
                return render(
                    request, "signup.html", {"username": username, "email": email}
                )
            if username_exists:
                return render(request, "signup.html", {"username": username})
            if email_exists:
                return render(request, "signup.html", {"email": email})

            user = User.objects.create_user(username, email, password)
            user.save()
            return redirect('user_login_handler')
        except IntegrityError as e:
            print("Error:", e)
            return render(request, "signup.html", {"username": username})

        finally:
            print("Do somethng")

#1
def reset_user_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user_otp = request.POST.get("otp")
        password = request.POST.get("password")
        try:
            email_exists = User.objects.filter(email=email).exists()
            print("BEFORE IF")
            user = User.objects.get(email=email)

            if password:
                # do update the password for the user
                # on sucessful updating, take the user to login
                #delete the otp(furher improvements)
                #user = User.objects.create_user(username, email, password)
                print(password)
                user.set_password(password)
                return redirect('user_login_handler')
        except Exception as e:
             return render(request, "OTP.html", {'email':email, 'is_email_exists':'false'})
            
        
        if user_otp:
            # check the otp with the database one
            print("Inside OTP")
            user_otp_obj = UserOTP.objects.get(user_email=email, user_otp=user_otp)
            print(user_otp_obj)
            print("USER")
            #if opt_obj.user_otp == user_otp:
            return render(request, "change_password.html", {'email':email})
        if email_exists:
            print("User exists")
            try:
                otp = generate_otp()
                print("OTP")
                print(otp)
                
              # otp_obj = 
                user_otp_obj, created = UserOTP.objects.update_or_create(
                user_email=email,
                defaults={"user_otp": otp}
            )
                print("saved otp n database")
                send_mail(
                    "OTP Youtify",
                    "Your one time password is :" + otp,
                    "ozonewagle998@gmail.com",
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                logging.error(f"Error sending test email: {e}")
                return HttpResponse(
                    "An error occurred while sending the test email.", status=500
                )

            return render(request, "OTP.html", {"email": email})

    return render(request, "OTP.html")

#2
# def reset_user_password(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         user_otp = request.POST.get("otp")
#         email_exists = User.objects.filter(email=email).exists()

#         if email_exists:
#             try:
#                 # Retrieve the User object based on the email
#                 user = User.objects.get(email=email)
#                 print("USSSER")
#                 print(user)

#                 # Create or update (effectively update here) UserOTP record
#                 user_otp, created = UserOTP.objects.update_or_create(
#                     user=user, defaults={"user_otp": "123456"}
#                 )
#                 print("SAVED")
#                 # Send email with OTP (assuming you have a send_mail function)
#                 send_mail(
#                     "OTP Youtify",
#                     "Your one time password is :" + user_otp,
#                     "ozonewagle998@gmail.com",  # Replace with your sender email
#                     [email],
#                     fail_silently=False,
#                 )

#             except User.DoesNotExist:
#                 # Handle the case where the email doesn't exist in User table
#                 return HttpResponse(
#                     "The email you entered does not exist. Please try again.",
#                     status=400,
#                 )

#             except Exception as e:
#                 # Handle potential errors during database operations or email sending
#                 logging.error(f"Error saving OTP or sending email: {e}")
#                 return HttpResponse(
#                     "An error occurred. Please try again later.", status=500
#                 )

#         # ... (rest of your code to handle GET requests or other scenarios)

#     return render(request, "OTP.html")


def playlist(request):
    cur_user = playlist_user.objects.get(username=request.user)
    try:
        song = request.GET.get("song")
        song = cur_user.playlist_song_set.get(song_title=song)
        song.delete()
    except:
        pass
    if request.method == "POST":
        add_playlist(request)
        return HttpResponse("")
    song = "kSFJGEHDCrQ"
    user_playlist = cur_user.playlist_song_set.all()
    # print(list(playlist_row)[0].song_title)
    return render(
        request, "playlist.html", {"song": song, "user_playlist": user_playlist}
    )


def search(request):
    if request.method == "POST":

        add_playlist(request)
        return HttpResponse("")
    try:
        search = request.GET.get("search")
        song = YoutubeSearch(search, max_results=10).to_dict()
        song_li = [song[:10:2], song[1:10:2]]
        # print(song_li)
    except:
        return redirect("/")

    return render(
        request, "search.html", {"CONTAINER": song_li, "song": song_li[0][0]["id"]}
    )


def add_playlist(request):
    cur_user = playlist_user.objects.get(username=request.user)

    if (request.POST["title"],) not in cur_user.playlist_song_set.values_list(
        "song_title",
    ):

        songdic = (YoutubeSearch(request.POST["title"], max_results=1).to_dict())[0]
        song__albumsrc = songdic["thumbnails"][0]
        cur_user.playlist_song_set.create(
            song_title=request.POST["title"],
            song_dur=request.POST["duration"],
            song_albumsrc=song__albumsrc,
            song_channel=request.POST["channel"],
            song_date_added=request.POST["date"],
            song_youtube_id=request.POST["songid"],
        )
