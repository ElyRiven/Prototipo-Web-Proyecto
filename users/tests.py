from django.test import TestCase
import unittest
from users.authentication import utils

class testEncryptPassword(unittest.TestCase):
    def testEncryptPassword(self):
        password = '123456'
        expectedHash = 'e10adc3949ba59abbe56e057f20f883e'
        self.assertEqual(utils.encryptPassword(password), expectedHash)