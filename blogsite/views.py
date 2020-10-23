from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User,Listing,Comment,Achievelist,Allblogs
from datetime import datetime

def index(request):
    items=Listing.objects.all()
    try:
        w = Achievelist.objects.filter(user=request.user.username)
        wcount=len(w)
    except:
        wcount=None
    return render(request, "blogsite/index.html",{
        "items":items,
        "wcount":wcount
    })

def categories(request):
    items=Listing.objects.raw("SELECT * FROM blogsite_listing GROUP BY category")
    try:
        w = Achievelist.objects.filter(user=request.user.username)
        wcount=len(w)
    except:
        wcount=None
    return render(request,"blogsite/categpage.html",{
        "items": items,
        "wcount":wcount
    })

def category(request,category):
    catitems = Listing.objects.filter(category=category)
    try:
        w = Achievelist.objects.filter(user=request.user.username)
        wcount=len(w)
    except:
        wcount=None
    return render(request,"blogsite/category.html",{
        "items":catitems,
        "cat":category,
        "wcount":wcount
    })

def create(request):
    try:
        w = Achievelist.objects.filter(user=request.user.username)
        wcount=len(w)
    except:
        wcount=None
    return render(request,"blogsite/create.html",{
        "wcount":wcount
    })

def submit(request):
    if request.method == "POST":
        listtable = Listing()
        now = datetime.now()
        dt = now.strftime(" %d %B %Y %X ")
        listtable.owner = request.user.username
        listtable.title = request.POST.get('title')
        listtable.description = request.POST.get('description')
        listtable.category = request.POST.get('category')
        if request.POST.get('link'):
            listtable.link = request.POST.get('link')
        else :
            listtable.link = "https://cdn.shopify.com/s/files/1/1061/1924/files/Hugging_Face_Emoji_2028ce8b-c213-4d45-94aa-21e1a0842b4d_large.png?15202324258887420558"
        listtable.time = dt
        listtable.save()
        all = Allblogs()
        items = Listing.objects.all()
        for i in items:
            try:
                if Allblogs.objects.get(listingid=i.id):
                    pass
            except:
                all.listingid=i.id
                all.title = i.title
                all.description = i.description
                all.link = i.link
                all.save()

        return redirect('index')
    else:
        return redirect('index')


def listingpage(request,id):
    try:
        item = Listing.objects.get(id=id)
    except:
        return redirect('index')
    try:
        comments = Comment.objects.filter(listingid=id)
    except:
        comments = None
    if request.user.username:
        try:
            if Achievelist.objects.get(user=request.user.username,listingid=id):
                added=True
        except:
            added = False
        try:
            l = Listing.objects.get(id=id)
            if l.owner == request.user.username :
                owner=True
            else:
                owner=False
        except:
            return redirect('index')
    else:
        added=False
        owner=False
    try:
        w = Achievelist.objects.filter(user=request.user.username)
        wcount=len(w)
    except:
        wcount=None
    return render(request,"blogsite/listingpage.html",{
        "i":item,
        "error":request.COOKIES.get('error'),
        "errorgreen":request.COOKIES.get('errorgreen'),
        "comments":comments,
        "added":added,
        "owner":owner,
        "wcount":wcount
    })



def cmntsubmit(request,listingid):
    if request.method == "POST":
        now = datetime.now()
        dt = now.strftime(" %d %B %Y %X ")
        c = Comment()
        c.comment = request.POST.get('comment')
        c.user = request.user.username
        c.time = dt
        c.listingid = listingid
        c.save()
        return redirect('listingpage',id=listingid)
    else :
        return redirect('index')

def addachived(request,listingid):
    if request.user.username:
        w = Achievelist()
        w.user = request.user.username
        w.listingid = listingid
        w.save()
        return redirect('listingpage',id=listingid)
    else:
        return redirect('index')


def removeachived(request,listingid):
    if request.user.username:
        try:
            w = Achievelist.objects.get(user=request.user.username,listingid=listingid)
            w.delete()
            return redirect('listingpage',id=listingid)
        except:
            return redirect('listingpage',id=listingid)
    else:
        return redirect('index')

def watchlistpage(request,username):
    if request.user.username:
        try:
            w = Achievelist.objects.filter(user=username)
            items = []
            for i in w:
                items.append(Listing.objects.filter(id=i.listingid))
            try:
                w = Achievelist.objects.filter(user=request.user.username)
                wcount=len(w)
            except:
                wcount=None
            return render(request,"blogsite/watchlistpage.html",{
                "items":items,
                "wcount":wcount
            })
        except:
            try:
                w = Achievelist.objects.filter(user=request.user.username)
                wcount=len(w)
            except:
                wcount=None
            return render(request,"blogsite/watchlistpage.html",{
                "items":None,
                "wcount":wcount
            })
    else:
        return redirect('index')

def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "blogsite/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "blogsite/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "blogsite/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "blogsite/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "blogsite/register.html")
