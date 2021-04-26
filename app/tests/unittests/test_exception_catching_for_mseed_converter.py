import unittest
from mseed_converter import convert_to_mseed
from azure.core.exceptions import ResourceNotFoundError
from exceptions import MSeedConvertionException


class TestMseedConverterExceptionsRaised(unittest.TestCase):
    def testWrongFilePath(self):
        wrong_azure_storage_decimated_file_path = "d/d/d/d/oseberg-test.ccs-oseberg.segy"
        with self.assertRaises(ResourceNotFoundError):
            convert_to_mseed(wrong_azure_storage_decimated_file_path, "oseberg")

    def testWrongFileName(self):
        wrong_azure_storage_decimated_file_path = "oseberg/2021/3/3/wrongfile"
        with self.assertRaises(ResourceNotFoundError):
            convert_to_mseed(wrong_azure_storage_decimated_file_path, "oseberg")

    def testWrongStationName(self):
        wrong_station_name = "graneosebergsnorre"
        decimated_file_path = "grane/2021/4/20/2021-03-02-17-05-23-Grane3579618.ccs-grane.dsgd"
        with self.assertRaises(MSeedConvertionException):
            convert_to_mseed(decimated_file_path, wrong_station_name)
