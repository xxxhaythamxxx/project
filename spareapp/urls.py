from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('find', views.find,name='find'),
    # path('chaining/', include('smart_selects.urls')),
    path("sparedetails/<str:val>",views.sparedetails,name="sparedetails"),
    # path("sparedetails/<str:val>?<str:val2>",views.sparedetails,name="sparedetails"),
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
    path("openCar",views.openCar,name="openCar"),
    path("shopCartFunction",views.shopCartFunction,name="shopCartFunction"),
    path("cartTotal/<str:val>",views.cartTotal,name="cartTotal"),
    path("fillcar",views.fillcar,name="fillcar"),
    path("fillengine",views.fillengine,name="fillengine"),
    path("fillspare",views.fillspare,name="fillspare"),
    path("fillcategoryadmin",views.fillcategoryadmin,name="fillcategoryadmin"),
    path("fillsubcategory",views.fillsubcategory,name="fillsubcategory"),
    path("fillbrand",views.fillbrand,name="fillbrand"),
    path("vendorSpareAjax",views.vendorSpareAjax,name="vendorSpareAjax"),
    path("editcar/<str:val>",views.editcar,name="editcar"),
    path("editengine/<str:val>",views.editengine,name="editengine"),
    path("editspare/<str:val>",views.editspare,name="editspare"),
    path("editecategory/<str:val>",views.editecategory,name="editecategory"),
    path("editebrand/<str:val>",views.editebrand,name="editebrand"),
    path("editemake/<str:val>",views.editemake,name="editemake"),
    path("editesubcategory/<str:val>",views.editesubcategory,name="editesubcategory"),
    path("listcar",views.listcar,name="listcar"),
    path("listbrand",views.listbrand,name="listbrand"),
    path("listcat",views.listcat,name="listcat"),
    path("listsubcat",views.listsubcat,name="listsubcat"),
    path("listspare",views.listspare,name="listspare"),
    path("listmake",views.listmake,name="listmake"),
    path("listList",views.listList,name="listList"),
    path("listengine",views.listengine,name="listengine"),
    path("deletecar/<str:val>",views.deletecar,name="deletecar"),
    path("deleteengine/<str:val>",views.deleteengine,name="deleteengine"),
    path("deletespare/<str:val>",views.deletespare,name="deletespare"),
    path("deletecategory/<str:val>",views.deletecategory,name="deletecategory"),
    path("deletemake/<str:val>",views.deletemake,name="deletemake"),
    path("deletebrand/<str:val>",views.deletebrand,name="deletebrand"),
    path("deletesubcategory/<str:val>",views.deletesubcategory,name="deletesubcategory"),
    path("fillcategory",views.fillcategory,name="fillcategory"),
    path("fillvendor",views.fillvendor,name="fillvendor"),
    path("importCar",views.importCar,name="importCar"),
    path("importEngine",views.importEngine,name="importEngine"),
    path("importSpare",views.importSpare,name="importSpare"),
    path("exportCategories",views.exportCategories,name="exportCategories"),
    path("openBrand",views.openBrand,name="openBrand"),
    path("importCategory",views.importCategory,name="importCategory"),
    path("register",views.register,name="register"),
    path("carEnginePlus",views.carEnginePlus,name="carEnginePlus"),
    path("login/",LoginView.as_view(template_name="spareapp/login.html"),name="login"),
    # path("contLogin/",LoginView.as_view(template_name="spareapp/contLogin.html"),name="contLogin"),
    path("contLogin/",views.contLogin,name="contLogin"),
    path("contLogout/",views.contLogout,name="contLogout"),
    path("logout/",LogoutView.as_view(template_name="spareapp/logout.html"),name="logout"),
    path("cart/<str:val>",views.cart,name="cart"),
    path("listAdmin",views.listAdmin,name="listAdmin"),
    path("userProfile/<str:val>",views.userProfile,name="userProfile"),
    path("deleteuser/<str:val>",views.deleteuser,name="deleteuser"),
    path("contBase",views.contBase,name="contBase"),
    path("contDay",views.contDay,name="contDay"),
    path("contEntry",views.contEntry,name="contEntry"),
    # re_path("contType/(?P<val>.*)$?<str:val2>",views.contType,name="contType"),
    path("contType/<str:val>?<str:val2>",views.contType,name="contType"),
    # path("contSpend",views.contSpend,name="contSpend"),
    path("contToPay",views.contToPay,name="contToPay"),
    path("contToCollect",views.contToCollect,name="contToCollect"),
    path("contAdmin",views.contAdmin,name="contAdmin"),
    path("contAddType",views.contAddType,name="contAddType"),
    path("contAddCategory",views.contAddCategory,name="contAddCategory"),
    path("contListCategory",views.contListCategory,name="contListCategory"),
    path("contListType",views.contListType,name="contListType"),
    path("contDeleteCategory/<str:val>",views.contDeleteCategory,name="contDeleteCategory"),
    path("contDeleteType/<str:val>",views.contDeleteType,name="contDeleteType"),
    # path("contEditType/<str:val>",views.contEditType,name="contEditType"),
    # path("contEditCategory/<str:val>",views.contEditCategory,name="contEditCategory"),
    path("contByDay",views.contByDay,name="contByDay"),
    path("contByDayCustom",views.contByDayCustom,name="contByDayCustom"),
    path("contByRange",views.contByRange,name="contByRange"),
    path("contByRangeCustom",views.contByRangeCustom,name="contByRangeCustom"),
    path("contCollectFac/<str:val>",views.contCollectFac,name="contCollectFac"),
    path("contPayFac/<str:val>",views.contPayFac,name="contPayFac"),
    path("contPayFacType/<str:val>?<str:val2>?<str:val3>",views.contPayFacType,name="contPayFacType"),
    path("contCollectFacType/<str:val>?<str:val2>?<str:val3>",views.contCollectFacType,name="contCollectFacType"),
    path("contTypeRange/<str:val>?<str:val2>?<str:val3>",views.contTypeRange,name="contTypeRange"),
    path("contTypeRangeTarjeta/<str:val>?<str:val2>?<str:val3>",views.contTypeRangeTarjeta,name="contTypeRangeTarjeta"),
    path("contAddPerson",views.contAddPerson,name="contAddPerson"),
    path("accountStat",views.accountStat,name="accountStat"),
    path("contTypeTarjeta/<str:val>?<str:val2>",views.contTypeTarjeta,name="contTypeTarjeta"),
    path("contThisMonth",views.contThisMonth,name="contThisMonth"),
    path("contLastMonth",views.contLastMonth,name="contLastMonth"),
    path("editeFact/<str:val>/<str:val2>",views.editeFact,name="editeFact"),
    path("contTotalDay",views.contTotalDay,name="contTotalDay"),
    path("contIndividual/<str:val>",views.contIndividual,name="contIndividual"),
    path("factTypeES",views.factTypeES,name="factTypeES"),
    path("sortMain",views.sortMain,name="sortMain"),
    path("sortToPay",views.sortToPay,name="sortToPay"),
    path("sortToCollect",views.sortToCollect,name="sortToCollect"),
    path("sortMain2",views.sortMain2,name="sortMain2"),
    path("contListByType/<str:val>",views.contListByType,name="contListByType"),
    path("contListByTypeZero",views.contListByTypeZero,name="contListByTypeZero"),
    re_path("contListByCategory/(?P<val>.*)$",views.contListByCategory,name="contListByCategory"),
    path("contListByCategoryZero",views.contListByCategoryZero,name="contListByCategoryZero"),
    path("contEditPerson/<str:val>",views.contEditPerson,name="contEditPerson"),
    path("accountDay",views.accountDay,name="accountDay"),
    path("deleteFac/<str:val>",views.deleteFac,name="deleteFac"),
    path("contAddTable",views.contAddTable,name="contAddTable"),
    path("customTables/<str:val>",views.customTables,name="customTables"),
    # path("customTables",views.customTables,name="customTables"),
    path("contListCustomTables",views.contListCustomTables,name="contListCustomTables"),
    # path("editeCustomTable/<str:val>",views.editeCustomTable,name="editeCustomTable"),
    re_path("editeCustomTable/(?P<val>.*)$",views.editeCustomTable,name="editeCustomTable"),
    # path("deleteCustom/<str:val>",views.deleteCustom,name="deleteCustom"),
    re_path("deleteCustom/(?P<val>.*)$",views.deleteCustom,name="deleteCustom"),
    path("customTablesRange/<str:val>?<str:val2>",views.customTablesRange,name="customTablesRange"),
    path("contDayBack/<str:val>",views.contDayBack,name="contDayBack"),
    path("contDayBackRange/<str:val>?<str:val2>",views.contDayBackRange,name="contDayBackRange"),
    # path("operacionesTablas",views.operacionesTablas,name="operacionesTablas"),
    path("searchTable",views.searchTable,name="searchTable"),
    path("contAddCliente",views.contAddCliente,name="contAddCliente"),
    path("contListClienteTables",views.contListClienteTables,name="contListClienteTables"),
    path("editeClienteTable/<str:val>",views.editeClienteTable,name="editeClienteTable"),
    path("deleteClienteTable/<str:val>",views.deleteClienteTable,name="deleteClienteTable"),
    path("contAddOperacion",views.contAddOperacion,name="contAddOperacion"),
    path("contListCustomTablesOp",views.contListCustomTablesOp,name="contListCustomTablesOp"),
    re_path("editeCustomTableOp/(?P<val>.*)$",views.editeCustomTableOp,name="editeCustomTableOp"),
    re_path("deleteCustomOp/(?P<val>.*)$",views.deleteCustomOp,name="deleteCustomOp"),
    re_path("deleteCustomOpCat/(?P<val>.*)$",views.deleteCustomOpCat,name="deleteCustomOpCat"),
    path("editeFactAccount/<str:val>/<str:val1>/<str:val2>",views.editeFactAccount,name="editeFactAccount"),
    path("contAddOperacionCat",views.contAddOperacionCat,name="contAddOperacionCat"),
    path("contListCustomTablesCat",views.contListCustomTablesCat,name="contListCustomTablesCat"),
    re_path("editeCustomTableCat/(?P<val>.*)$",views.editeCustomTableCat,name="editeCustomTableCat"),
    # re_path("deleteCustomCat/(?P<val>.*)$",views.deleteCustomCat,name="deleteCustomCat"),
    path("contTypeCat/<str:val>?<str:val2>",views.contTypeCat,name="contTypeCat"),
    path("contTypeRangeCat/<str:val>?<str:val2>?<str:val3>",views.contTypeRangeCat,name="contTypeRangeCat"),
    # path("contTypeRangeTarjeta/<str:val>?<str:val2>?<str:val3>",views.contTypeRangeTarjeta,name="contTypeRangeTarjeta"),
    # path("contTypeTarjeta/<str:val>?<str:val2>",views.contTypeTarjeta,name="contTypeTarjeta"),
    # path('getCar/$', views.getCar,name="getCar")
    path("probarRepetido",views.probarRepetido,name="probarRepetido"),
    path("combinarUsuarios",views.combinarUsuarios,name="combinarUsuarios"),
    path("respaldarDb",views.respaldarDb,name="respaldarDb"),
    path("contCargarDb",views.contCargarDb,name="contCargarDb"),
    path("cargarDb",views.cargarDb,name="cargarDb"),
    path("checkearNc",views.checkearNc,name="checkearNc"),
    path("deleteDb",views.deleteDb,name="deleteDb"),
    path("deleteDbSpare",views.deleteDbSpare,name="deleteDbSpare"),
    path("filterToCollect",views.filterToCollect,name="filterToCollect"),
    path("filterContType",views.filterContType,name="filterContType"),
    path("filterContTypeTarjeta",views.filterContTypeTarjeta,name="filterContTypeTarjeta"),
    path("filterContTypeCat",views.filterContTypeCat,name="filterContTypeCat"),
    path("totalTablasType",views.totalTablasType,name="totalTablasType"),
    path("filterAccountStat",views.filterAccountStat,name="filterAccountStat"),
    path("totalAccountStat",views.totalAccountStat,name="totalAccountStat"),
    path("filterAccountDay",views.filterAccountDay,name="filterAccountDay"),
    path("subCategoria",views.subCategoria,name="subCategoria"),
    path("spareCat",views.spareCat,name="spareCat"),
    path("filltrans",views.filltrans,name="filltrans"),
]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)