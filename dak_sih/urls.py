"""dak_sih URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from philatelist.urls import router as pr
from forum.urls import router as fr
from store.urls import product_router, collection_router, order_router
from dak_exchange.urls import router as exchange_router
from dashboard.urls import router as dashboard_router
from services.urls import router as services_router

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('schema/', SpectacularAPIView.as_view(), name="schema"),
    path('schema/docs/', SpectacularSwaggerView.as_view(url_name="schema")),
    
    path('philatelist/', include(pr.urls)),
    path('forum/', include(fr.urls)),
    
    path('product/', include(product_router.urls)),
    path('collection/', include(collection_router.urls)),
    path('order/', include(order_router.urls)),
    
    path('exchange/', include(exchange_router.urls)),
    path('services/', include(services_router.urls)),
    
    path('dashboard/', include(dashboard_router.urls)),
]

# TODO: add urls for media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)