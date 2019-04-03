from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.core.files.base import ContentFile
from google.cloud import storage
from .serializers import FileSerializer
from .preprocess import preprocessFCSToCSV
from .models import File
from .utils import upload_blob, getAllFilesFromBucket
from google.cloud import storage

class FileView(APIView):

    parser_classes = (MultiPartParser, FormParser,FileUploadParser)

    def get(self, request, *args, **kwargs):

        files = getAllFilesFromBucket('flowcytometry.appspot.com')
        return JsonResponse({'files': files})

    def post(self, request, *args, **kwargs):

        # bucket_name = 'flowcytometry.appspot.com'
        files = request.data.getlist('file')
        # client = storage.Client()
        # bucket = client.get_bucket('flowcytometry.appspot.com')

        for file in files:
            print(file)
            print(type(file))

        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            for file in files:
                if hasattr(file, 'name'):
                    print(file.name + "inside the data")
                    # blob = bucket.blob('FCS/' + file.name)
                    # blob.upload_from_filename(file)
                    data = default_storage.save(file.name,  ContentFile(file.read()))
                    # preprocessFCSToCSV(file_serializer.data, file.name)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PreProcessView(APIView):

    # parser_classes = (MultiPartParser, FormParser, FileUploadParser)

    def post(self, request, *args, **kwargs):
        print(request.data)
        files = request.data['selectedFiles']
        print(files)
        for file in files:
            preprocessFCSToCSV(file)
        return Response({}, status=status.HTTP_201_CREATED)
