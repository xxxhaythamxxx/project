from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('find', views.find,name='find'),
    path('chaining/', include('smart_selects.urls')),
    path("sparedetails/<str:val>",views.sparedetails,name="sparedetails"),
    path("brand/<str:val>",views.brand,name="brand"),
    path("name/<str:val>",views.name,name="name"),
    path("manuf/<str:val>",views.manuf,name="manuf"),
    path("allmanu/<str:val>",views.allmanu,name="allmanu"),
    path("allmodel/<str:val>",views.allmodel,name="allmodel"),
    path("model/<str:val>",views.model,name="model"),
    path("engine/<str:val>",views.enginel,name="engine"),
    path('detail',views.detail,name='detail'),
    path("shape/<str:val>",views.shape,name="shape"),
    path("longi/<str:val>",views.longi,name="longi"),
    path("widei/<str:val>",views.widei,name="widei"),
    path("highi/<str:val>",views.highi,name="highi"),
    path("diameteri/<str:val>",views.diameteri,name="diameteri"),
    path("radioi/<str:val>",views.radioi,name="radioi"),
    # path("cilinder/<str:val>",views.cilinder,name="cilinder"),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)