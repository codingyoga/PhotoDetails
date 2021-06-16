# standard imports
import datetime
import uuid
import csv
from subprocess import check_call
from urllib.parse import urlparse
import time
import logging
# 3rd party import
import requests
# user defined modules
import upload_to_s3
import settings

END_POINT_URL = "https://jsonplaceholder.typicode.com/photos"

# Header of tsv file
HEADERS = ['photo_id','title','url','timestamp']

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

def fetch_data():
    """Fetch JSON data from this endpoint: https://jsonplaceholder.typicode.com/photos

    Returns:
        [dict]: returning data got from endpoint 
    """
    try:
        photo_data = requests.get(url=END_POINT_URL).json()
        if photo_data:
            logging.info(f"successfully fetched data from url {END_POINT_URL}")
            return photo_data
        else:
            logging.error(f"No data, check url {END_POINT_URL}") 
            exit(1)         
    except requests.exceptions.RequestException as e:
        logging.error(f"Error in fetching data from url {e}")
        raise

def process_data(photo_data, photo_file_name):
    """[summary]

    Args:
        photo_data (dict): data got from the url 
        photo_file_name (String): file name for tsv file format photos_YYYY-MM-DD_uuid4 
    """
    logging.info("processing data")
    try:
        with open(photo_file_name, 'w', newline='') as tsv_file:
            tsv_writer = csv.writer(tsv_file, delimiter='\t')
            tsv_writer.writerow(HEADERS)
            for each_data in photo_data:
                each_row = list()               
                # for column photo_id concatenating albumId and id with underscore
                each_row.append(str(each_data.get('albumId'))+'_'+str(each_data.get('id')))               
                # for column title
                each_row.append(each_data.get('title'))
                # extracting only path, params, query and fragment of url 
                parsed_url = urlparse(each_data.get('url'))
                add_query = f'?{parsed_url.query}' if parsed_url.query else ''
                each_row.append(f'{parsed_url.path}{parsed_url.params}{add_query}{parsed_url.fragment}')
                # for column timestamp
                each_row.append(datetime.datetime.now().isoformat())
                tsv_writer.writerow(each_row)
    except Exception as e:
        logging.error("Error while processing data writing as tcv")
        exit(1)


def photo_details():
    """Main funtion which has 4 steps - fetch data , process data ,Gzip tsv 
    and upload file to s3 bucket 
    """
    photo_data = fetch_data()

    # tsv file name format "photos_YYYY-MM-DD_uuid4"
    unique_id = uuid.uuid4()
    photo_file_name = f'photos_{datetime.date.today()}_{unique_id}.tsv'
    photo_file_name_gz = f"{photo_file_name}.gz"
    
    # Process data and create tsv file 
    process_data(photo_data, photo_file_name)

    # Gzip the TSV
    check_call(['gzip', photo_file_name])
    logging.info("tsv file converted into gzip")

    # Upload file to S3 bucket
    upload_success = upload_to_s3.upload_file(photo_file_name_gz, settings.BUCKET_NAME)
    if upload_success:
        logging.info(f"uploaded to s3 filename is {photo_file_name_gz}")
        logging.info(f"s3 uri is s3://{settings.BUCKET_NAME}/{photo_file_name_gz}" )
    else:
        logging.error(f"failed to upload to s3 {photo_file_name_gz}")
    
    return photo_file_name_gz

if __name__ == "__main__":
    start_time = time.time() 
    photo_details()
    # capture end time
    end_time = time.time()
    logging.info(f"code execution time in seconds {(end_time - start_time)}")
