from fcsparser import parse
import csv
from google.cloud import storage
from pandas import ExcelWriter
import os
from FC_Backend import settings
from google.cloud import storage

def preprocessFCSToCSV(filedata, filename):
    print(filedata)

    # Initialise a client
    storage_client = storage.Client("FlowCytometry")
    # Create a bucket object for our bucket
    bucket = storage_client.get_bucket('flowcytometry.appspot.com')
    # Create a blob object from the filepath
    blob = bucket.blob(filename)
    # Download the file to a destination
    os.path.join(settings.BASE_DIR, 'media')
    blob.download_to_filename(settings.BASE_DIR+'/tmp.fcs')

    path =  settings.BASE_DIR + '/tmp.fcs'

    meta, data = parse(path, meta_data_only=False, reformat_meta=True)

    with open('fcs_file.csv', mode='w') as fcs_file:
        fcs_writer = csv.writer(fcs_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for index, row in data.iterrows():
            print(row['FL1-A'], row['FL3-A'])
            fcs_writer.writerow([row['FL1-A'], row['FL3-A']])




