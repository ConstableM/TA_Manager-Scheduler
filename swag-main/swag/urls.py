"""
URL configuration for swag project.

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls')
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from ta_manager.views import Home, Account, CourseView, SectionView, CreateWhat, CreateUser, CreateCourse, CreateSection

urlpatterns = [
	path('', Home.as_view()),
	path('admin/', admin.site.urls),
	path('create/', CreateWhat.as_view(), name='Create'),
	path('create/user/', CreateUser.as_view()),
	path('create/course/', CreateCourse.as_view()),
	path('create/section/', CreateSection.as_view()),
	path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True)),
	path('logout/', auth_views.LogoutView.as_view(), name='Log Out'),
	path('account/', Account.as_view(), name='Account'),
	path('course/', CourseView.as_view(), name='Course'),
	path('section/', SectionView.as_view(), name='Section'),
]
