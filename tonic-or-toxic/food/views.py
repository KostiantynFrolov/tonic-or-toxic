from django.views import View
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponse, render, redirect
from .forms import (SignupForm, LoginForm, SearchAdditiveForm, SearchAdditivesForm,
                    SelectLanguageForm)
from .models import ToxicantEN, ToxicantPL, Toxicant
from django.contrib import messages
from paddleocr import PaddleOCR
import os
import tkinter
from tkinter import filedialog


class HomepageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return render(request, 'homepage.html')


class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'signup.html'
    success_url = reverse_lazy('dashboard')


class LoginView(View):
    form = LoginForm
    html = 'login.html'

    def get(self, request):
        return render(request, self.html, {'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password')
                return render(request, self.html, {'form': self.form})
        else:
            return render(request, self.html, {'form': self.form})


class LogoutView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        logout(request)
        return redirect('homepage')


class DashboardView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        return render(request, 'dashboard.html')


class SearchAdditiveView(LoginRequiredMixin, View):
    login_url = '/login_url'
    form = SearchAdditiveForm
    html = 'search_additive.html'

    def get(self, request):
        return render(request, self.html, {'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            if form.cleaned_data['language'] == '1':
                result = ToxicantEN.objects.filter(names__icontains=form.cleaned_data['additive_name'].strip()).first()
                if result:
                    result = Toxicant.objects.get(toxicant_en=result)
            else:
                result = ToxicantPL.objects.filter(names__icontains=form.cleaned_data['additive_name'].strip()).first()
                if result:
                    result = Toxicant.objects.get(toxicant_pl=result)
            return render(request, 'result.html', {'result': result})
        else:
            return render(request, self.html, {'form': form})


class SearchAdditivesView(SearchAdditiveView):
    form = SearchAdditivesForm
    html = 'search_additives.html'

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            additive_names_split = form.cleaned_data['additive_names'].split(',')
            results = []
            if form.cleaned_data['language'] == '1':
                for additive_name in additive_names_split:
                    result = ToxicantEN.objects.filter(names__icontains=additive_name.strip()).first()
                    if result:
                        result = Toxicant.objects.get(toxicant_en=result)
                        results.append(result)
            else:
                for additive_name in additive_names_split:
                    result = ToxicantPL.objects.filter(names__icontains=additive_name.strip()).first()
                    if result:
                        result = Toxicant.objects.get(toxicant_pl=result)
                        results.append(result)
            return render(request, 'results.html', {'results': set(results)})
        else:
            return render(request, self.html, {'form': form})


class AdditiveDetailsView(LoginRequiredMixin, View):
    def get(self, request, additive_id):
        return render(request, 'result.html', {'result': Toxicant.objects.get(id=additive_id)})


class SearchAdditivesByPhoto(LoginRequiredMixin, View):
    login_url = '/login_url'
    form = SelectLanguageForm
    html = 'search_additives_by_photo.html'

    def get(self, request):
        root = tkinter.Tk()
        root.withdraw()
        image_path = filedialog.askopenfilename()
        return render(request, self.html, {'form': self.form, 'image_path': image_path})



















