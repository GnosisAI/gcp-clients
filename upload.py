from google.cloud import storage
storage_client = storage.Client()
bucket_name = 'uploads-zk'
def upload_blob( source_file_name, destination_blob_name):

    print(f"begin uploading file {source_file_name}")
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))