from django.urls import path

from .views import ApiKeyView, RegistrationView, LoginView, RestaurantsView


app_name = 'authentication'
urlpatterns = [
    path('register/', RegistrationView.as_view({'post': 'register'})),
    path('login/', LoginView.as_view({'post': 'login'})),
    path('api_keys/', ApiKeyView.as_view({'get': 'apikey'})),
    path('restaurants/', RestaurantsView.as_view({'post': 'list'})),

]
