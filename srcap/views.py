from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import os
import csv
import shutil

from srcap.models import ScrapyData
from srcap.serializers import ScrapyDataSerializer


class DataSaveView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def post(self, request):
        downloads_path = '/home/tarif/Downloads/'
        data_list = []

        try:
            with open('folder_path.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == 'path':
                        continue

                    links_text = row[1]
                    downloads_folder = os.path.expanduser('~/Downloads')

                    file_names = [f for f in os.listdir(downloads_path) if f.startswith(str(links_text))]
                    saved_files = [f for f in os.listdir(row[0])]
                    print('saved_files ======================= ', saved_files)

                    for file_name in file_names:
                        if file_name not in saved_files:
                            print('file_name =================== ', file_name)

                            current_directory = row[0]
                            print('current_directory ================ ', current_directory)

                            source_file = os.path.join(downloads_folder, file_name)
                            destination_file = os.path.join(current_directory, file_name)

                            shutil.move(source_file, destination_file)

                            fpath = current_directory + file_name
                            print('fpath ========================= ', fpath)

                            data_obj = None
                            data_obj = ScrapyData()
                            data_obj.data_type = '.tsv'
                            data_obj.path = fpath
                            data_list.append(data_obj)


            ScrapyData.objects.bulk_create(data_list)
            print("Data created successfully!")
            return Response({"message": "Data created!", "data": {}}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("Exception ================ ", e)
        return Response({"message": "Data not created!", "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class DataUpdateView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ScrapyDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": "Data not valid!", "data": {}}, status=status.HTTP_400_BAD_REQUEST)

        serializer_data = serializer.data
        data_id = request.data['id']

        try:
            ScrapyData.objects.data_update(data_id, serializer_data)
            return Response({"message": "Data updated sucessfully.", "data": {}}, status=status.HTTP_200_OK)

        except Exception as e:
            print('serializer_data ================== ', serializer_data)

        return Response({"message": "Data not updated!", "data": {}}, status=status.HTTP_400_BAD_REQUEST)
