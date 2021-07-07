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
    path('', Learning.views.learning_index),  # 主页
    path('train/', Learning.views.train_index),  # 训练
    path('result/', Learning.views.task_list_index),  # 结果 -- 任务列表
    path('result/clean', Learning.views.clean),  # 结果 -- 清理
    path('result/<int:page>/', Learning.views.task_list_index),  # 结果 -- 任务列表
    path('result/<int:page>/<str:anything>/', Learning.views.task_list_index),  # 结果 -- 任务列表
    path('result/<int:page>/<int:item>/log/', Learning.views.log_index),  # 结果 -- 日志
    path('result/<int:page>/<int:item>/analysis/', Learning.views.analysis_index),  # 结果 -- 分析
    path('result/<int:page>/<int:item>/delete/', Learning.views.delete),  # 结果 -- 删除
    path('post/', Learning.views.post),  # 上传
    path('admin/', admin.site.urls),  # 管理
]
