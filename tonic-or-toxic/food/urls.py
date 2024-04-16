from django.urls import path

from .views import (AddHarmfulProductView, AdditiveDetailsView, DashboardView,
                    HomepageView, LoginView, LogoutView,
                    SearchAdditivesByPhotoWizard, SearchAdditivesView,
                    SearchAdditiveView, ShowHarmfulProductsView, SignupView)

app_name = "food"
urlpatterns = [
    path("",
         HomepageView.as_view(),
         name="homepage"),
    path("signup/",
         SignupView.as_view(),
         name="signup"),
    path("login/",
         LoginView.as_view(),
         name="login"),
    path("logout/",
         LogoutView.as_view(),
         name="logout"),
    path("dashboard/",
         DashboardView.as_view(),
         name="dashboard"),
    path("search-additive/",
         SearchAdditiveView.as_view(),
         name="search_additive"),
    path("search-additives/",
         SearchAdditivesView.as_view(),
         name="search_additives"),
    path("additive-details/<int:additive_id>/",
         AdditiveDetailsView.as_view(),
         name="additive_details"),
    path("search-additives-by-photo/",
         SearchAdditivesByPhotoWizard.as_view(),
         name="search_additives_by_photo"),
    path("add-harmful-product/<str:toxicants_ids>/",
         AddHarmfulProductView.as_view(),
         name="add_harmful_product"),
    path("show-harmful-products/",
         ShowHarmfulProductsView.as_view(),
         name="show_harmful_products")
]
