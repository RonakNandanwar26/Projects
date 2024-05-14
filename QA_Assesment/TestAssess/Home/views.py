from django.shortcuts import render
from django.http import HttpResponseRedirect,JsonResponse
from utility.pdf_utility import *
from rest_framework.views import APIView 
from rest_framework.response import Response
import os
from django.views.generic import TemplateView



class UploadPDF(TemplateView):
    template_name = 'pdf_upload.html'

    def post(self,request):
        pdf_file = request.FILES['pdf_file']
        typ = request.POST['type'] 
        print(typ)
        success, response_message = handle_uploaded_pdf(pdf_file)
       
        QA,final_QA = extract_pdf_text('media/uploaded_pdfs/Test Attempt Student.pdf',typ)
        
        print(QA)
        errors = evaluate_pdf(QA,typ)
        print(errors)
        if len(errors) == 0:
            success = True
        else:
            success = False
            response_message = "PDF upload failed, Please do the suggested changes and upload again..."

        if success:
            return render(request, 'pdf_upload.html', {'response_message': response_message, 'success': True})
        else:
            return render(request, 'pdf_upload.html', {'response_message': response_message, 'success': False, 'errors': errors})

    def get(self, request):
        return render(request, self.template_name)


def upload_pdf(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        typ = request.POST['type'] 
        print(typ)
        success, response_message = handle_uploaded_pdf(pdf_file)
       
        QA,final_QA = extract_pdf_text('media/uploaded_pdfs/Test Attempt Student.pdf',typ)
        
        print(QA)
        errors = evaluate_pdf(QA,typ)
        print(errors)
        if len(errors) == 0:
            success = True
        else:
            success = False
            response_message = "PDF upload failed, Please do the suggested changes and upload again..."
        if success:
            return render(request, 'pdf_upload.html', {'response_message': response_message, 'success': True})
        else:
            return render(request, 'pdf_upload.html', {'response_message': response_message, 'success': False, 'errors':errors})

    return render(request, 'pdf_upload.html')
    

def handle_uploaded_pdf(pdf_file):
    try:
        # Specify the directory where you want to save the uploaded PDFs
        upload_dir = 'media/uploaded_pdfs/'
        os.makedirs(upload_dir, exist_ok=True)

        # Open a file in binary mode and write the uploaded PDF content
        with open(os.path.join(upload_dir, pdf_file.name), 'wb') as destination:
            for chunk in pdf_file.chunks():
                destination.write(chunk)

        return True, "File uploaded successfully."
    except Exception as e:
        return False, f"Error uploading file: {str(e)}"
