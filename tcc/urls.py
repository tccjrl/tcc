"""tcc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from hosts.views import homeView, listaHost, novoHost, atualizaHost, deletaHost, listaTemplate, novoTemplate, atualizaTemplate, \
    deletaTemplate, listaItem, novoItem, atualizaItem, deletaItem, getData

urlpatterns = [
    path('admin/', admin.site.urls),
    # ==================================================================================================================
    path('', homeView, name='url_home'),
    path('api/data/', getData, name='api_data'),
    # ==================================================================================================================
    path('lista_host/', listaHost, name='url_cadastroHost'),
    path('novo_host/', novoHost, name='url_novoHost'),
    path('atualiza_host/<int:pk>/', atualizaHost, name='url_atualizaHost'),
    path('deleta_host/<int:pk>/', deletaHost, name='url_deletaHost'),
    # ==================================================================================================================
    path('lista_template/', listaTemplate, name='url_listaTemplate'),
    path('novo_template/', novoTemplate, name='url_novoTemplate'),
    path('atualiza_template/<int:pk>/', atualizaTemplate, name='url_atualizaTemplate'),
    path('deleta_template/<int:pk>/', deletaTemplate, name='url_delataTemplate'),
    # ==================================================================================================================
    path('lista_item/', listaItem, name='url_listaItem'),
    path('novo_item/', novoItem, name='url_novoItem'),
    path('atualiza_item/<int:pk>/', atualizaItem, name='url_atualizaItem'),
    path('deleta_item/<int:pk>/', deletaItem, name='url_deletaItem'),
]
