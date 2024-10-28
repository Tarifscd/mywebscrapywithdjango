import os
import csv
import shutil
from django.urls import reverse
from unittest import mock
from rest_framework import status
from rest_framework.test import APITestCase
from .models import ScrapyData
from .serializers import ScrapyDataSerializer

class DataSaveViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('data-save')  # Update with the actual URL name for DataSaveView.

    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data="path,links_text\nfolder1/,link1\nfolder2/,link2\n")
    @mock.patch("os.listdir")
    @mock.patch("shutil.move")


    def test_data_creation_successful(self, mock_move, mock_listdir, mock_open):
        mock_listdir.side_effect = [
            ["link1_file.tsv"],
            ["link2_file.tsv"],
            []
        ]

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ScrapyData.objects.first().data_type, ".tsv")
        self.assertIn("Data created!", response.data["message"])

    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data="path,links_text\nfolder1,link1\nfolder2,link2\n")
    @mock.patch("os.listdir")


    def test_data_creation_no_new_files(self, mock_listdir, mock_open):
        mock_listdir.side_effect = [
            ["link1_file.tsv"],
            ["link1_file.tsv"],
            ["link2_file.tsv"]
        ]

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ScrapyData.objects.count(), 0)
        self.assertIn("Data not created!", response.data["message"])

    @mock.patch("builtins.open", side_effect=Exception("File not found"))


    def test_data_creation_file_not_found(self, mock_open):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Data not created!", response.data["message"])

    @mock.patch("builtins.open", new_callable=mock.mock_open, read_data="path,links_text\nfolder1,link1\n")
    @mock.patch("os.listdir", side_effect=Exception("Directory error"))


    def test_data_creation_directory_error(self, mock_listdir, mock_open):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Data not created!", response.data["message"])


class DataUpdateViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('data-update')
        self.scrapy_data = ScrapyData.objects.create(
            data_type=".csv",
            path="test_path/file.csv"
        )
        self.valid_data = {
            "id": self.scrapy_data.id,
            "data_type": ".tsv",
            "path": "new_test_path/file.tsv"
        }
        self.invalid_data = {
            "id": self.scrapy_data.id,
            "data_type": "",
            "path": "new_test_path/file.tsv"
        }

    @mock.patch("srcap.models.ScrapyData.objects.data_update")
    def test_data_update_success(self, mock_data_update):
        mock_data_update.return_value = None

        response = self.client.post(self.url, self.valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Data updated successfully.", response.data["message"])

    def test_data_update_invalid_data(self):
        response = self.client.post(self.url, self.invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Data not valid!", response.data["message"])

    @mock.patch("srcap.models.ScrapyData.objects.data_update")
    def test_data_update_failure(self, mock_data_update):
        mock_data_update.side_effect = Exception("Update failed")

        response = self.client.post(self.url, self.valid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Data not updated!", response.data["message"])
