from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Trip
import bcrypt
# Create your views here.
def index(request):
    return redirect('/main')

def main(request):
    return render(request,'main.html')

def register(request):
    errors = User.objects.user_validator(request.POST)
        
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/main')

    else:
        hashpw= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(username=request.POST['username'],name=request.POST['name'],password=hashpw)
        usern = request.POST['username']
        newuser=User.objects.get(username=usern)
        request.session['userid'] = newuser.id
        return redirect('/travels')

def login(request):
    # login verirification/authorization
    errors = {}

    usern = User.objects.filter(username=request.POST['username'])
    if not usern:
        errors['username'] = "Username or Password is Invalid!"
    else:
        logged_user= usern[0]
        if bcrypt.checkpw(request.POST['password'].encode(),logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect("/travels")
        else:
            errors['password'] = "Username or Password is Invalid!"

    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request,value)
            return redirect("/main")

def travels(request):
    if 'userid' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['userid'])
    usertrips = user.trips.all()
    context = {
        'user': user,
        'alltrips': Trip.objects.all(),
        'usertrips': usertrips
    }
    return render(request,'travels.html', context)

def logout(request):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        del request.session['userid']
        return redirect('/')

def add(request):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        return render(request,'addtravel.html')

def addtravel(request):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        errors = Trip.objects.trip_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/travels/add')
        else:
            currentuser = User.objects.get(id=request.session['userid'])
            trip = Trip.objects.create(creator=currentuser,destination=request.POST['destination'],description=request.POST['description'],startdate=request.POST['startdate'],enddate=request.POST['enddate'])
            trip.user.add(currentuser)
            return redirect('/travels')

def destination(request, id):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        trip = Trip.objects.get(id=id)
        user = User.objects.get(id=request.session['userid'])
        
        
        context = {
            'trip': trip,
            'user': user

        }
        return render(request,'destination.html', context)

def join(request, id):
    if 'userid' not in request.session:
        return redirect('/')
    else:
        trip = Trip.objects.get(id=id)
        user = User.objects.get(id=request.session['userid'])
        trip.user.add(user)
        return redirect('/travels')

        

