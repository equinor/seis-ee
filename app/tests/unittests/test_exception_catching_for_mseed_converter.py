import unittest
from mseed_converter import convert_to_mseed
from azure.core.exceptions import ResourceNotFoundError
from exceptions import BadInputException


class TestMseedConverterExceptionsRaised(unittest.TestCase):
    def testWrongFilePath(self):
        wrong_azure_storage_decimated_file_path = "d/d/d/d/oseberg-test.ccs-oseberg.segy"
        self.assertRaises(ResourceNotFoundError, convert_to_mseed, wrong_azure_storage_decimated_file_path)

    def testWrongFileName(self):
        wrong_azure_storage_decimated_file_path = "oseberg/2021/3/3/wrongfile"
        self.assertRaises(ResourceNotFoundError, convert_to_mseed, wrong_azure_storage_decimated_file_path)
