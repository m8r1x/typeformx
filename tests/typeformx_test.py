import os
import sys
path = '/'.join(os.getcwd().split('/')[:-1])+'/typeformx'
sys.path.insert(0, path)

from mock import Mock, patch
from nose.tools import assert_is_not_none
import requests

from typeformx import TypeformX

api_key = "5035e5b14ab1fcef829642edca63b512fdb9a86d"

typeform = TypeformX(api_key, True)

@patch('typeformx.requests.get')
def test_request_response(mock_get):
    mock_get.return_value.ok = True
    assert_is_not_none(typeform.get_all_forms())