#from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import FileUpload
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from lxml import etree

from django.http import HttpResponse
import uuid
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv()

def apikey_OK(apikey):
    if apikey is None:
        return False
    SECRET_APIKEY = os.environ.get('SECRET_APIKEY')
    print("Apikey on {}".format(SECRET_APIKEY))
    return apikey == SECRET_APIKEY

class FileSerializer(serializers.HyperlinkedModelSerializer):
    #file = serializers.FileField()
    class Meta:
        model = FileUpload
        fields = ['file']

class InfoViewSet(viewsets.ViewSet):
    def list(self, request):
        return HttpResponse("Welcome to opensource project called challenge_multipurpose_api! The project is still in progress, but we hope you enjoy your stay!")

class WeatherViewSet(viewsets.ViewSet):
    def list(self, request):
        return HttpResponse("It's raining.. maybe? Not implemented yet..")

class FeaturesViewSet(viewsets.ViewSet):
    def list(self, request):
        return HttpResponse("WIP: Not very feature rich project..")

class ApiViewSet(viewsets.ViewSet):
    """
    Get apikey
    """
    def list(self, request):
        return render(request, 'api.html')

class FileViewSet(viewsets.ViewSet):
    """
    Simple view which renders xml for internal usage
    """

    # def list(self, request):
    #     # queryset = FileUpload.objects.all()
    #     # serializer = FileSerializer(queryset, many=True)
    #     # print(serializer.data)
    #     return Response("GET file not implemented yet")
    #     #return Response(serializer.data)

    def create(self, request):
        if not apikey_OK(request.META.get('HTTP_APIKEY')):
            return HttpResponse('APIKEY either not included or incorrect, use with e.g. curl -H "APIKEY: 123123" ...\n')
        
        raw_data = request.FILES['file']
        file_bytestring = raw_data.read()
        #file_string = file_bytestring.decode('utf-8')

        parser = etree.XMLParser(no_network=False, load_dtd=True, resolve_entities=True)

        doc = etree.fromstring(file_bytestring, parser=parser)
        result = "OK"
        return Response(result)

class SaveXmlViewSet(viewsets.ViewSet):
    """
    Simple view which saves user inputted file to .dtd -file and 
    returns response with the path and filename
    """
    base_path = os.getcwd() + "/api_stuff/uploads/"

    # def create_directory_for_uuid(self, user_id):
    #     path = self.base_path + user_id
    #     try:
    #         os.mkdir(path)
    #     except OSError:
    #         print("Creation of the directory %s failed" % path)
    #     else:
    #         print("Successfully created the directory %s " % path)
    #         return path
    # def create(self, request):
    #     raw_data = request.FILES['file']
    #     file_bytestring = raw_data.read()
    #     file_string = file_bytestring.decode('utf-8')
    #     path = None

    #     # Set uuid cookie for user if it doesnt exists
    #     user_id = request.COOKIES.get('user_id')
    #     if user_id is None:
    #         user_id = str(uuid.uuid4())
    #         path = self.create_directory_for_uuid(user_id)
    #     else:
    #         path = self.base_path + user_id

    #     filename = '/filename.dtd'
    #     full_path = path + filename
    #     with open(full_path, 'w', encoding='utf-8') as f:
    #         f.write(file_string)
    #     print("File was written succesfully ", path, filename)
    #     response = HttpResponse('File was saved succesfully to\n{}\n'.format(full_path))
    #     response.set_cookie('user_id', user_id)
    #     return response

    

    def create(self, request):
        if not apikey_OK(request.META.get('HTTP_APIKEY')):
            return HttpResponse('APIKEY either not included or incorrect, use with e.g. curl -H "APIKEY: 123123" ...\n')

        request_file = request.FILES['file']
        print(request_file.size)

        if not request_file:
            return HttpResponse('File is missing')

        MAX_SIZE_IN_BYTES = 1000
        if request_file.size >= MAX_SIZE_IN_BYTES:
            return HttpResponse('File size exceeds the allowed size of {} bytes'.format(MAX_SIZE_IN_BYTES))

        raw_data = request_file

        file_bytestring = raw_data.read()
        if "https://" in str(file_bytestring):
            return HttpResponse('No can do, no TLS certificate installed')
        print(file_bytestring)
        file_string = file_bytestring.decode('utf-8')

        user_id = str(uuid.uuid4())

        filename = user_id + '.dtd'
        full_path = self.base_path + filename
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(file_string)
        print("File was written succesfully ", full_path)
        response = HttpResponse('File was saved succesfully to\n{}\n'.format(full_path))
        return response
