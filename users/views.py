from django.shortcuts import redirect, render
from .forms import CustomerRegisterForm
from store.models import Customer
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            Customer.objects.create(user=new_user, email=new_user.email, name=new_user.username, budget=1000000)
            return redirect('login')
    form = CustomerRegisterForm()
    return render(request, 'users/register.html', {'form':form})

@login_required
def logout(request):
    django_logout(request)
    return render(request, 'users/logout.html')
