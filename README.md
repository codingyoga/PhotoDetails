# PhotoDetails

Appplication is to 
- Fetch data from https://jsonplaceholder.typicode.com/photos
- Process json data 
- Create TSV file with columns "photo_id, title, url, timestamp"
- Gzip the TSV
- Upload file to S3 bucket

Configurable AWS Credentials and s3 Bucket
---------------
Add your ACCESS_KEY and SECRET_KEY in settings.py
```
ACCESS_KEY = ""
SECRET_KEY = ""

BUCKET_NAME = "photo-details-2021"
```

To Run
-------
```pip3.6 install -r requirements.txt
   python3.6 photo_details.py
```


Testing - To run pytest in docker
-------
make test 


Output
--------
![image](https://github.com/codingyoga/PhotoDetails/blob/7a326cc3dc75b1d652e28cac7c5575b02fdee805/screenshots/make%20run%20output.png)


Pytest and Test Coverage 
--------
![image](https://github.com/codingyoga/PhotoDetails/blob/f23397c2d29ab93458e293d705a2f75b9554d687/screenshots/testcases%20and%20coverage.png)


Troubleshooting
-------
- if ```make: *** [test] Error 1``` Please set SECRET_KEY and ACCESS_KEY in settings.py.
- python version used is 3.6

