from .models import User,Wishlist
from django.shortcuts import render,redirect
from django.contrib import messages
import bcrypt



def index(request):
    if 'user_id' not in request.session:
        return render(request, "index.html")
    else:
        return redirect('/login_success')

def display_register(request):
    return render(request, "display_register.html")

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.register_validator(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/display_register')
    else:
        
        new_user = User.objects.register(request.POST)
             
        return redirect('/')

def register_success(request):
    
    return render(request,"register_success.html")

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['username'], request.POST['password']):
        messages.error(request, 'Invalid Username/Password')
        return redirect('/')
    user = User.objects.get(username=request.POST['username'])
    request.session['user_id'] = user.id
    
    return redirect('/login_success')

def logout(request):
    request.session.clear()
    return redirect('/')

def login_success(request):
    user =User.objects.get(id=request.session['user_id'])
    context = {
        "user":user,
        "wishlisted_items": user.wishlisted_items.all(),
        "all_items": Wishlist.objects.all()
    }

    return render(request,"dashboard.html",context)

def show_create_item(request):
    context = {
        
    	"user": User.objects.get(id=request.session['user_id'])
    }

    return render(request,"create_item.html",context)

def create_item(request):
    errors = Wishlist.objects.wishlist_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login_success')
    else:
        user = User.objects.get(id=request.session["user_id"])
        item = Wishlist.objects.create(
            item_name = request.POST['item_name'],
            creator = user
        )
        # bonus: the book creator automatically
        
        user.wishlisted_items.add(item)
        return redirect('/login_success')
        #return redirect(f'/wish_items/{user.id}')

def add_to_wishlist(request,id):
    item_to_add = Wishlist.objects.get(id=id)
    user = User.objects.get(id=request.session["user_id"])
    user.wishlisted_items.add(item_to_add)
    return redirect('/login_success')

def remove_item(request,id):
    item = Wishlist.objects.get(id=id)
    user_to_remove_from = User.objects.get(id=request.session["user_id"])
    user_to_remove_from.wishlisted_items.remove(item)
    return redirect('/login_success')

def delete_item(request,id):
    item = Wishlist.objects.get(id=id)
    item.delete()
    return redirect('/login_success')


def display_item(request,id):
    context = {   
    	"item": Wishlist.objects.get(id=id)
    }
    return render(request,"display_item.html",context)





