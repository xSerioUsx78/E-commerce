from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/api-auth/', include('rest_framework.urls')),

    path('api/order/', include('order_app.urls')),
    path('api/address/', include('address_app.urls')),
    path('api/product/', include('product_app.api.urls')),
    path('api/review/', include('review_app.urls')),
    path('api/question-answer/', include('question_answer_app.urls')),
]


DEBUG = getattr(settings, "DEBUG", False)

if DEBUG:
    from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('docs/',
             SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
        path('redoc/',
             SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
