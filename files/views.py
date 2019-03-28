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
from .utils import upload_blob

class FileView(APIView):

    parser_classes = (MultiPartParser, FormParser,FileUploadParser)

    def get(self, request, *args, **kwargs):
        # Initialise a client
        storage_client = storage.Client("FlowCytometry")
        # Create a bucket object for our bucket
        bucket = storage_client.get_bucket('flowcytometry.appspot.com')
        print(type(bucket))
        blobs = bucket.list_blobs()

        for blob in blobs:
            print(blob.name)
        return JsonResponse({'foo': 'bar'})

    def post(self, request, *args, **kwargs):

        bucket_name = 'fcsfiles'
        files = request.data.getlist('file')
        for file in files:
            print(file)
            print(type(file))

        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            for file in files:
                if hasattr(file, 'name'):
                    print(file.name)
                    data = default_storage.save('FCS/'+file.name,  ContentFile(file.read()))
                    preprocessFCSToCSV(file_serializer.data, file.name)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)