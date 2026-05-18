from django.shortcuts import render,redirect

# Create your views here.
from django.contrib import messages
from .forms import CreateUserForm

def userRegister(request):
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}')
            return redirect('users:login')
    else:
        form=CreateUserForm()
    return render(request,'userRegister.html',{'form':form, 'hide_nav':True})   


# def login(request):
#     return render(request,'login.html')    


from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import AuthenticationForm

def userLogin(request):
    if request.method=='POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('product:index')
    else:
        form=AuthenticationForm()
    return render(request,'login.html',{'form':form,'hide_nav':True})    



from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    messages.success(request,'Logged out successfully')
    return redirect('users:login')


from  .models import Profile
def profile_form(request):
    ob,created=Profile.objects.get_or_create(user=request.user)
    if request.method=='POST':
        email=request.POST.get('email')
        city=request.POST.get('city')
        phone=request.POST.get('phone')

        ob.email=email
        ob.city=city
        ob.phone=phone
        ob.save()
        return redirect('users:profiledetails')
    return render(request,'profile.html',{'ob':ob})


from django.shortcuts import redirect

def profile(request):
    if not request.user.is_authenticated:
        return redirect('users:login')

    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile_details.html', {'profile': profile})



# from django.contrib.auth.decorators import login_required

# @login_required(login_url='login')
# def profile(request):
#     profile, created = Profile.objects.get_or_create(user=request.user)
#     return render(request, 'profile_details.html', {'profile': profile})