from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import os
import csv
import shutil

from srcap.models import ScrapyData
from srcap.serializers import ScrapyDataSerializer

from django.core.cache import cache
import logging
logger = logging.getLogger(__name__)

class DataSaveView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            downloads_path = '/home/tarif/Downloads/'
            data_list = []
            reader_data = []

            with open('folder_path.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == 'path':
                        continue
                    reader_data.append([str(row[0]), str(row[1])])

            print('reader_data ========================== ', reader_data)
            for row in reader_data:
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
                        print('data_list ========================= ', data_list)


            print('data_list 2 ========================= ', data_list)
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
        logger.debug("This is a debug message. =======================>>> ")
        logger.exception("This is a exception message. =======================>>> ")
        logger.info("This is an info message. =======================>>> ")
        logger.warning("This is a warning message. =======================>>> ")
        logger.error("This is an error message. =======================>>> ")
        logger.critical("This is a critical message. =======================>>> ")


        # Set a value in the cache
        cache.set('my_key', 'my_value', timeout=60 * 10) # Cache for 10 minutes
        cache.set('my_key2', {'my_value1': 1, 'my_value2': 2}, timeout=60 * 10)
        cache.set('my_key3', ['list1', 2, 3.4, True], timeout=60 * 10)

        # Get a value from the cache
        value = cache.get('my_key')
        print("value 1 ================================= ", value)  # Output: 'my_value'

        value2 = cache.get('my_key2')
        print("value 2 ================================= ", value2)

        value3 = cache.get('my_key3')
        print("value 3 ================================= ", value3)

        # Delete a value from the cache
        cache.delete('my_key')
        cache.delete('my_key2')
        cache.delete('my_key3')
        value = cache.get('my_key')
        print("value 4 ================================= ", value)
        value2 = cache.get('my_key2')
        print("value 5 ================================= ", value2)
        value3 = cache.get('my_key3')
        print("value 6 ================================= ", value3)

        serializer = ScrapyDataSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"message": "Data not valid!", "data": {}}, status=status.HTTP_400_BAD_REQUEST)

        serializer_data = serializer.data
        data_id = request.data['id']

        try:
            ScrapyData.objects.data_update(data_id, serializer_data)
            return Response({"message": "Data updated successfully.", "data": {}}, status=status.HTTP_200_OK)

        except Exception as e:
            print('exeptions ================== ', e)

        return Response({"message": "Data not updated!", "data": {}}, status=status.HTTP_400_BAD_REQUEST)
