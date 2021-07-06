"""Website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import Learning.views

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', Learning.views.learning_index),
    path('train/', Learning.views.train_index),
    path('result/', Learning.views.result_index),
    path('result/<int:page>/', Learning.views.result_index),
    path('result/<int:page>/<int:item>/', Learning.views.result_index),
    path('result/<int:page>/<int:item>/<str:want>/', Learning.views.result_index),
    path('post/', Learning.views.post),
    path('admin/', admin.site.urls),
]
