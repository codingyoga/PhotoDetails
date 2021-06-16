import photo_details
import requests 
from subprocess import check_call
import csv
import uuid
import datetime
import pytest

@pytest.fixture(scope="module")
def shared_tsv_file():
    tsv_file = photo_details.photo_details()
    return tsv_file

def test_tsv_file_created(shared_tsv_file):
    assert shared_tsv_file != None 

def test_count_of_photos(shared_tsv_file):
    """validate number of items processed which is fetched from URL 
    """
    expected_count = len(requests.get("https://jsonplaceholder.typicode.com/photos").json())
    tsv_file = shared_tsv_file
    check_call(['gunzip', tsv_file])
    tsv_file = tsv_file.split('.')[0]
    with open(f"{tsv_file}.tsv", 'r') as tsv_file:
        reader = csv.reader(tsv_file)
        actual_count= len(list(reader))
    # including + 1 header in tsv 
    assert expected_count+1 == actual_count

def test_filename(shared_tsv_file):
    tsv_file = shared_tsv_file
    tsv_file_name = tsv_file.split('.')[0]
    actual_file_format = tsv_file_name.split('_') 
    assert "photos" == actual_file_format[0]
    assert datetime.datetime.strptime(actual_file_format[1], '%Y-%m-%d')
    assert uuid.UUID(actual_file_format[2])
    
    




