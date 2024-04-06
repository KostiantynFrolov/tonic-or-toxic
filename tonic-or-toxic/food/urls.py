from django.urls import path
from .views import (HomepageView, SignupView, LoginView, LogoutView,
                    DashboardView, SearchAdditiveView, SearchAdditivesView,
                    AdditiveDetailsView, SearchAdditivesByPhoto)

urlpatterns = [
    path("", HomepageView.as_view(), name="homepage"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("search-additive/", SearchAdditiveView.as_view(), name="search_additive"),
    path("search-additives/", SearchAdditivesView.as_view(), name="search_additives"),
    path("additive-details/<int:additive_id>", AdditiveDetailsView.as_view(), name="additive_details"),
    path("search-additives-by-photo", SearchAdditivesByPhoto.as_view(), name="search_additives_by_photo")
]