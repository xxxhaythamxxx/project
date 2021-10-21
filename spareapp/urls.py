from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('find', views.find,name='find'),
    path('chaining/', include('smart_selects.urls')),
    path("sparedetails/<str:val>?<str:val2>",views.sparedetails,name="sparedetails"),
    path("brand/<str:val>",views.brand,name="brand"),
    path("name/<str:val>",views.name,name="name"),
    path("manuf/<str:val>",views.manuf,name="manuf"),
    path("allmanu/<str:val>",views.allmanu,name="allmanu"),
    path("allmodel/<str:val>",views.allmodel,name="allmodel"),
    path("model/<str:val>",views.model,name="model"),
    path("engine/<str:val>",views.enginel,name="engine"),
    path('detail',views.detail,name='detail'),
    path("shape/<str:val>",views.shape,name="shape"),
    path("longi/<str:val1>?<str:val2>",views.longi,name="longi"),
    path("atributes/<str:val1>?<str:val2>",views.atributes,name="atributes"),
    path("carBrands",views.carBrands,name="carBrands"),
    # path("categoryi",views.categoryi,name="categoryi"),
    path("categoryi/<str:val>",views.categoryi,name="categoryi"),
    re_path("categoryi/(?P<val>.*)$",views.categoryi,name="categoryi"),
    # ['categoryi/(?P<val>)$', 'categoryi/(?P<val>[^/]+)$']
    path("chasis/<str:val>",views.chasis,name="chasis"),
    path("prev/<str:val>?<str:val2>",views.prev,name="prev"),
    path("next/<str:val>?<str:val2>",views.next,name="next"),
    path("filldb",views.filldb,name="filldb"),
    path("fillcar",views.fillcar,name="fillcar"),
    path("fillengine",views.fillengine,name="fillengine"),
    path("fillspare",views.fillspare,name="fillspare"),
    path("editcar/<str:val>",views.editcar,name="editcar"),
    path("editengine/<str:val>",views.editengine,name="editengine"),
    path("editspare/<str:val>",views.editspare,name="editspare"),
    path("listcar",views.listcar,name="listcar"),
    path("listspare",views.listspare,name="listspare"),
    path("listengine",views.listengine,name="listengine"),
    path("deletecar/<str:val>",views.deletecar,name="deletecar"),
    path("deleteengine/<str:val>",views.deleteengine,name="deleteengine"),
    path("deletespare/<str:val>",views.deletespare,name="deletespare"),
    path("fillcategory",views.fillcategory,name="fillcategory"),
    path("fillvendor",views.fillvendor,name="fillvendor"),
    path("importCar",views.importCar,name="importCar"),
    path("importEngine",views.importEngine,name="importEngine"),
    path("importSpare",views.importSpare,name="importSpare"),
    path("register",views.register,name="register"),
    path("login/",LoginView.as_view(template_name="spareapp/login.html"),name="login"),
    path("logout/",LogoutView.as_view(template_name="spareapp/logout.html"),name="logout"),
    path("cart/<str:val>",views.cart,name="cart"),
    path("listAdmin",views.listAdmin,name="listAdmin"),
    path("userProfile/<str:val>",views.userProfile,name="userProfile"),
    path("deleteuser/<str:val>",views.deleteuser,name="deleteuser"),
    path("contBase",views.contBase,name="contBase"),
    path("contDay",views.contDay,name="contDay"),
    path("contEntry",views.contEntry,name="contEntry"),
    path("contType/<str:val>?<str:val2>",views.contType,name="contType"),
    path("contSpend",views.contSpend,name="contSpend"),
    path("contToPay",views.contToPay,name="contToPay"),
    path("contToCollect",views.contToCollect,name="contToCollect"),
    path("contAdmin",views.contAdmin,name="contAdmin"),
    path("contAddType",views.contAddType,name="contAddType"),
    path("contAddCategory",views.contAddCategory,name="contAddCategory"),
    path("contListCategory",views.contListCategory,name="contListCategory"),
    path("contListType",views.contListType,name="contListType"),
    path("contDeleteCategory/<str:val>",views.contDeleteCategory,name="contDeleteCategory"),
    path("contDeleteType/<str:val>",views.contDeleteType,name="contDeleteType"),
    path("contEditType/<str:val>",views.contEditType,name="contEditType"),
    path("contEditCategory/<str:val>",views.contEditCategory,name="contEditCategory"),
    path("contByDay",views.contByDay,name="contByDay"),
    path("contByRange",views.contByRange,name="contByRange"),
    path("contCollectFac/<str:val>",views.contCollectFac,name="contCollectFac"),
    path("contPayFac/<str:val>",views.contPayFac,name="contPayFac"),
    path("contTypeRange/<str:val>?<str:val2>?<str:val3>",views.contTypeRange,name="contTypeRange"),
    path("contTypeRangeTarjeta/<str:val>?<str:val2>?<str:val3>",views.contTypeRangeTarjeta,name="contTypeRangeTarjeta"),
    path("contAddPerson",views.contAddPerson,name="contAddPerson"),
    path("accountStat",views.accountStat,name="accountStat"),
    path("contTypeTarjeta/<str:val>?<str:val2>",views.contTypeTarjeta,name="contTypeTarjeta"),
    path("contThisMonth",views.contThisMonth,name="contThisMonth"),
    path("contLastMonth",views.contLastMonth,name="contLastMonth"),
    path("editeFact/<str:val>",views.editeFact,name="editeFact"),
    path("contTotalDay",views.contTotalDay,name="contTotalDay"),
    path("contIndividual/<str:val>",views.contIndividual,name="contIndividual"),
    path("factTypeES",views.factTypeES,name="factTypeES"),

    # path('getCar/$', views.getCar,name="getCar")
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)