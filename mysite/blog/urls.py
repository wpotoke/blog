from django.urls import path
from blog import views

app_name = "blog"

urlpatterns = [
    path("<int:id>/", views.post_detail, name="post_detail"),
    path("", views.post_list, name="post_list"),
]
