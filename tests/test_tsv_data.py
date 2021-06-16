import photo_details
from subprocess import check_call
import csv
import datetime

import pytest

@pytest.fixture(scope="module")
def shared_tsv_file():
    tsv_file = photo_details.photo_details()
    check_call(['gunzip', tsv_file])
    tsv_file = tsv_file.split('.')[0]
    return tsv_file

def test_tsv_header_columns(shared_tsv_file):
    expected_headers = ['photo_id','title','url','timestamp']
    tsv_file = shared_tsv_file
    with open(f"{tsv_file}.tsv", 'r') as tsv_file:
        reader = csv.reader(tsv_file)
        actual_headers_tsv = list(reader)[0]
    actual_headers = actual_headers_tsv[0].split('\t')  
    assert expected_headers == actual_headers   

def test_column_photo_id(shared_tsv_file):
    fixture_data = [
    {
    "albumId": 1,
    "id": 1,
    "title": "accusamus beatae ad facilis cum similique qui sunt",
    "url": "https://via.placeholder.com/600/92c952",
    "thumbnailUrl": "https://via.placeholder.com/150/92c952"
    }]
    expected_photo_id = f"{fixture_data[0]['albumId']}_{fixture_data[0]['id']}"
    
    tsv_file = shared_tsv_file
    with open(f"{tsv_file}.tsv", 'r') as tsv_file:
        reader = csv.reader(tsv_file)
        actual_row_tsv = list(reader)[1]
    actual_photo_id = actual_row_tsv[0].split('\t')[0] 
    assert expected_photo_id == actual_photo_id

def test_column_url(shared_tsv_file):
    fixture_data = [
    {
    "albumId": 1,
    "id": 1,
    "title": "accusamus beatae ad facilis cum similique qui sunt",
    "url": "https://via.placeholder.com/600/92c952",
    "thumbnailUrl": "https://via.placeholder.com/150/92c952"
    }]
    expected_url = '/'+fixture_data[0].get('url').split("//")[1].split('/',1)[1]
    tsv_file = shared_tsv_file
    with open(f"{tsv_file}.tsv", 'r') as tsv_file:
        reader = csv.reader(tsv_file)
        actual_row_tsv = list(reader)[1]
    actual_url = actual_row_tsv[0].split('\t')[2] 
    assert expected_url == actual_url

def test_column_timestamp(shared_tsv_file):
    tsv_file = shared_tsv_file
    with open(f"{tsv_file}.tsv", 'r') as tsv_file:
        reader = csv.reader(tsv_file)
        actual_row_tsv = list(reader)[1]
    actual_data_time = actual_row_tsv[0].split('\t')[3]
    expected_format_string = '%Y-%m-%dT%H:%M:%S.%f'
    assert datetime.datetime.strptime(actual_data_time, expected_format_string)
    