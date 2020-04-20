from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, userUpdateForm, profileUpdateForm
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm

# Create your views here.
# here request is sent in register as input and if the request method is post then validate and create a from with that data
def register(request):
    if request.method == 'POST':
        # take the request.POST data and create a form.. for the down line below
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # below one saves the user
            form.save()
            # username = form.cleaned_data.get('username')   ..this can be used to say "username you are logged in"
            # this below one is a flashback message, f stands for flashback( i.e alert )
            # the second parameter is the message.. here the message won't be displayed 
            # it is just initiated.. it will be displayed in a html page.. here blog-home.. and home extends to base
            messages.success(request, f'Your account has been created! You can login now')
            # redirect to blog-home(the name we gave to home page of blog) 
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def sample_view(request):
    current_user = request.user
    context={
        'current_user': current_user,
    }
    return render(request,'users/test.html')

@login_required  #this is a decorator i.e a function... i.e if user is logged in only then go to profile 
def profile(request):
    if request.method == 'POST':
        u_form=userUpdateForm(request.POST,instance=request.user)
        p_form=profileUpdateForm(request.POST,request.FILES,instance=request.user.profile)#here request.FILES as image file will come
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile has been updated')
            return redirect('profile') 
    else:
        u_form=userUpdateForm(instance=request.user)
        p_form=profileUpdateForm(instance=request.user.profile)
    context={
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request,'users/profile.html',context)