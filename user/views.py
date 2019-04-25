from django.shortcuts import render
from django.views import View
from django.views.generic import FormView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
#
from .forms import UserForm, UserCreationForm, LoginForm

# Create your views here.
class Index(View):
    def get(self, request):
        # return HttpResponse('<h2>Index in user</h2>')
        return render(request, 'user_index.html')

class UserSelf(View):
    def get(self, request):
        user = authenticate(request)

        return render(request, 'user_self.html', {'title':'個人檔案'})

class UserLogin(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = '/user/self/'

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return redirect('/user/login/')
    #     return super().dispatch(request,*args, **kwargs)

    def form_valid(self, form):
        self.request.session.set_expiry(43200) # 12 hours
        login(self.request, form.get_user())
        return redirect(self.success_url)

class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect('/user/login/')
    def post(self, request):
        return self.get(self, request)

class UserRegister(FormView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = '/user/login/'

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)
