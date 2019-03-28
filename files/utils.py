from google.cloud import storage
from fcsparser import parse
import csv
import six
from pandas import ExcelWriter

def upload_blob(bucket_name, file, destination_blob_name, content_type):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    storage.Blob.upload_from_file()

    bucket = storage_client.get_bucket(bucket_name)

    blob = bucket.blob(destination_blob_name)


    blob.upload_from_string(
        file,
        content_type=content_type)

    url = blob.public_url
    if isinstance(url, six.binary_type):
        url = url.decode('utf-8')

    return url

    # blob.upload_from_filename(source_file_name)
    #
    # print('File {} uploaded to {}.'.format(
    #     source_file_name,
    #     destination_blob_name))


def createPreprocessedFile(filePath,filename):
    # path = '/home/karthik/Desktop/HKR/SustainableProjects/A01 LF14in.c11 S.fcs'

    meta, data = parse(filePath, meta_data_only=False, reformat_meta=True)

    with open(filename + '.csv', mode='w') as fcs_file:
        fcs_writer = csv.writer(fcs_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for index, row in data.iterrows():
            print(row['FL1-A'], row['FL3-A'])
        fcs_writer.file


