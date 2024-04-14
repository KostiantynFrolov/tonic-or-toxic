from django.core.files.storage.filesystem import FileSystemStorage
from django.views import View
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import HttpResponse, render, redirect
from .forms import (SignupForm, LoginForm, SearchAdditiveForm, SearchAdditivesForm,
                    SelectLanguageForm, ImageForm, ProductForm)
from .models import ToxicantEN, ToxicantPL, Toxicant, Product
from django.contrib import messages
from django.conf import settings
from formtools.wizard.views import SessionWizardView
import os
from PIL import Image
import pytesseract
import re



class HomepageView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("food:dashboard")
        else:
            return render(request, "homepage.html")


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "signup.html"
    success_url = reverse_lazy("food:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Congratulations! Your signup is complete. "
                                       "You can now log in.")
        return response



class LoginView(View):
    form = LoginForm
    html = "login.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.html, {"form": self.form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                messages.success(request, "Congratulations! You have successfully logged in.")
                return redirect("food:dashboard")
            else:
                messages.error(request, "Invalid username or password!")
                return render(request, self.html, {"form": self.form})
        else:
            return render(request, self.html, {"form": self.form})


class LogoutView(LoginRequiredMixin, View):
    login_url = "food:login"

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("food:homepage")


class DashboardView(LoginRequiredMixin, View):
    login_url = "food:login"

    def get(self, request, *args, **kwargs):
        return render(request, "dashboard.html")


class SearchAdditiveView(LoginRequiredMixin, View):
    login_url = "food:login"
    form = SearchAdditiveForm
    html = "search_additive.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.html, {"form": self.form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            if form.cleaned_data["language"] == "en":
                result = ToxicantEN.objects.filter(names__icontains=form.cleaned_data["additive_name"].strip()).first()
                if result:
                    result = Toxicant.objects.get(toxicant_en=result)
            else:
                result = ToxicantPL.objects.filter(names__icontains=form.cleaned_data["additive_name"].strip()).first()
                if result:
                    result = Toxicant.objects.get(toxicant_pl=result)
            return render(request, "result.html", {"result": result})
        else:
            return render(request, self.html, {"form": form})


def check_food_additives(request, language, food_additives):
    results = []
    if language == "en":
        for food_additive in food_additives:
            result = ToxicantEN.objects.filter(names__icontains=food_additive.strip()).first()
            if result:
                result = Toxicant.objects.get(toxicant_en=result)
                results.append(result)
    else:
        for food_additive in food_additives:
            result = ToxicantPL.objects.filter(names__icontains=food_additive.strip()).first()
            if result:
                result = Toxicant.objects.get(toxicant_pl=result)
                results.append(result)
    results_id = ",".join([str(tox.id) for tox in set(results)]) if results else ""
    return render(request, "results.html", {"results": set(results),
                                            "results_id": results_id})


class SearchAdditivesView(SearchAdditiveView):
    form = SearchAdditivesForm
    html = "search_additives.html"

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            additive_names_split = form.cleaned_data["additive_names"].split(",")
            return check_food_additives(self.request, language=form.cleaned_data["language"],
                                 food_additives=additive_names_split)
        else:
            return render(request, self.html, {"form": form})


class AdditiveDetailsView(LoginRequiredMixin, View):
    login_url = "food:login"
    def get(self, request, additive_id):
        return render(request, "result.html", {"result": Toxicant.objects.get(pk=additive_id)})


class SearchAdditivesByPhotoWizard(LoginRequiredMixin, SessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "wizard_upload"))
    login_url = "food:login"
    form_list = [SelectLanguageForm, ImageForm]

    def get_template_names(self):
        templates = ["search_additives_by_photo_1.html", "search_additives_by_photo_2.html"]
        return [templates[int(self.steps.current)]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        if self.steps.current == "1":
            cleaned_data = self.get_cleaned_data_for_step("0")
            language = cleaned_data["language"]
            context["language"] = language
        return context

    def done(self, form_list, *args, **kwargs):
        form_data = [form.cleaned_data for form in form_list]
        language = form_data[0]['language']
        image_form = form_list[1]
        image = image_form.save()
        image_path = image.image.url.replace(settings.MEDIA_URL, settings.MEDIA_ROOT)

        with Image.open(image_path) as img:
            pillow_image_grey = img.convert("L")
            threshold = 128
            pillow_image_final = pillow_image_grey.point(lambda x: 0 if x < threshold else 255, "1")
            pillow_image_final.save(image_path)


        additives_beginning_pattern_polish = r"Sk(ł|t|l)adniki(:|.|S)"
        additives_beginning_pattern_english = "Ingredients:"
        if language == 'en':
            lang_rec = 'eng'
            additives_beginning_pattern = additives_beginning_pattern_english
        else:
            lang_rec = 'pol'
            additives_beginning_pattern = additives_beginning_pattern_polish
        recognized_text = pytesseract.image_to_string(image_path, lang=lang_rec, config="--psm 6")
        os.remove(image_path)
        image.delete()

        recognized_text_from_ingredients = ""

        for beginning in additives_beginning_pattern:
            if beginning in recognized_text:
                recognized_text_from_ingredients = recognized_text.split(beginning)[1]
        if not recognized_text_from_ingredients:
            return HttpResponse("Beginning of additives is not recognized")
        recognized_text_prepared = recognized_text_from_ingredients.split(".")[0]

        recognized_text_final = (recognized_text_prepared.replace("*", "").replace("'", "").replace("\"", "")
                .replace("emulsifier:", "").replace("emulgator:", "").replace(",,", ",")
                .replace("’", "").replace("”", "").replace("substancje konserwujące:", ""))

        base_list_of_additives = recognized_text_final.split(",")
        list_of_additives = [item.replace("\n", " ") for item in base_list_of_additives]
        """return render(self.request, 'done.html', {
                    'language': language,
                    'lang_rec': lang_rec,
                    'recognized_text': recognized_text,
                    'recognized_text_from_ingredients': recognized_text_from_ingredients,
                    'recognized_text_prepared': recognized_text_prepared,
                    'recognized_text_final': recognized_text_final,
                    'list_of_additives': list_of_additives})"""
        return check_food_additives(self.request, language=language, food_additives=list_of_additives)


class AddHarmfulProductView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'food:login'
    permission_required = "food.add_product"
    form_class = ProductForm
    template_name = 'add_product.html'
    success_url = reverse_lazy('food:show_harmful_products')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        toxicants_ids = self.kwargs.get("toxicants_ids")
        if toxicants_ids:
            toxicant_ids_list = [int(tox_id) for tox_id in toxicants_ids.split(",")]
            kwargs["toxicants_ids"] = toxicant_ids_list
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Congratulations! You have successfully"
                                       " added the harmful product.")
        return response


class ShowHarmfulProductsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = "food:login"
    permission_required = "food.add_product"
    template_name = "show_harmful_products.html"

    def get(self, request, *args, **kwargs):
        return render(request, "show_harmful_products.html",
                      {"products": Product.objects.all()})



