from django.contrib import messages
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from opp.forms import LoginForm
from django.contrib import messages
from django.views.generic import View
from django.shortcuts import render, redirect


from django.cls.mail import  EmailMessage 
from django.template.loader import render_to_string
from opp.forms import  LoginForm, RegisterForm
from opp.models import User
from opp.views.token import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
# opp/views/auth.py






def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
            else:
                messages.add_message(
                    request,
                    level=messages.WARNING,
                    message='User not found'
                )

    return render(request, 'opp/auth/login.html', {'form': form})





class RegisterPageView(View):
    template_name = 'opp/auth/register.html'
    form_class = RegisterForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, {'form': form, 'message': message })
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(first_name=first_name, email=email, password=password)
            user.is_active = False
            user.is_staff = True
            user.is_superuser = True
            user.save()
      
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
        
        return render(request, 'opp/auth/register.html', {'form': form})