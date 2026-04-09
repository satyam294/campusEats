from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "CampusEats — admin"
admin.site.site_title = "CampusEats"
admin.site.index_title = "Manage outlets, orders & accounts"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("orders/", include("orders.urls")),
    path("payments/", include("payments.urls")),
    path("", include("restaurant.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
