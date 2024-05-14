from django.urls import path
from .views import *

urlpatterns = [
    # path('upload/', UploadPDFTemplate.as_view(), name='upload_pdf'),
    path('upload_pdf/',UploadPDF.as_view(),name='upload_pdf_api')
]