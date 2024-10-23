from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
# myapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import os

from srcap.models import ScrapyData


class DataSaveView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    # Handle POST requests
    def post(self, request):
        print("here ============================= ")

        # Define the path to the directory
        # downloads_path = '/home/tarif/Downloads/'
        base_path = os.getcwd() + '/' +'srcap/management/commands/'

        # Check if the directory exists
        if os.path.exists(base_path):
            print(f"Directory exists: {base_path}")
        else:
            print(f"Directory does not exist: {base_path}")


        # List files in the directory
        # files = os.listdir(downloads_path)
        # print("Files in the directory:", files)

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

        book_data = request.data
        # Normally, you would validate and save the data to the database
        return Response({"message": "Book created!", "data": book_data}, status=status.HTTP_201_CREATED)
