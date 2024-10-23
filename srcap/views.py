from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
# myapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import os

from srcap.models import ScrapyData
from srcap.serializers import ScrapyDataSerializer


class DataSaveView(APIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [AllowAny]

    # Handle POST requests
    def post(self, request):
        base_path = os.getcwd() + '/' +'srcap/management/commands/'

        if os.path.exists(base_path):
            print(f"Directory exists: {base_path}")
        else:
            print(f"Directory does not exist: {base_path}")

        directory = base_path

        # List all folders in the directory
        folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

        print('folders ================== ', folders)
        data_list = []

        for dir in folders:
            if str(dir) == '__pycache__':
                continue
            downloads_path_root = base_path + str(dir) + '/'

            downloads_paths = [f for f in os.listdir(downloads_path_root) if os.path.isdir(os.path.join(downloads_path_root, f))]

            print('downloads_paths ==================== ', downloads_paths)
            for downloads_path in downloads_paths:
                if str(downloads_path) == '__pycache__':
                    continue

                tsv_files = [f for f in os.listdir(downloads_path_root + downloads_path + '/')]
                print("TSV files: ========================= ", tsv_files)

                for f in tsv_files:
                    fpath = downloads_path_root + downloads_path + '/' + str(f)
                    print('fpath ========================= ', fpath)

                    data_obj = None
                    data_obj = ScrapyData()
                    data_obj.data_type = '.tsv'
                    data_obj.path = fpath
                    data_list.append(data_obj)

        print('data_list -============================ ', data_list)
        ScrapyData.objects.bulk_create(data_list)

        print("Data created successfully!")

        return Response({"message": "Data created!", "data": {}}, status=status.HTTP_201_CREATED)


class DataUpdateView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    # Handle POST requests
    def post(self, request):
        serializer = ScrapyDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": "Data not valid!", "data": {}}, status=status.HTTP_400_BAD_REQUEST)

        serializer_data = serializer.data
        print('serializer_data ================== ', serializer_data)
        data_id = request.data['id']

        try:
            ScrapyData.objects.data_update(data_id, serializer_data)
            return Response({"message": "Data updated sucessfully.", "data": {}}, status=status.HTTP_200_OK)

        except Exception as e:
            pass

        return Response({"message": "Data not updated!", "data": {}}, status=status.HTTP_400_BAD_REQUEST)
