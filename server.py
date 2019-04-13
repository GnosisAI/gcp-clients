from google.cloud import storage
from flask import Flask, render_template, request, jsonify
from werkzeug import secure_filename
import os
import sys
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2
app = Flask(__name__) 
# global vars
storage_client = storage.Client()
bucket_name = 'uploads-zk'
model_id = "ICN2708198090334566848"
project_id = "unified-skein-232719"
name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
prediction_client = automl_v1beta1.PredictionServiceClient()


def upload_blob( source_file_name, destination_blob_name):

    print(f"begin uploading file {source_file_name}")
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


def predict_malaria(file):

    content = file.read()
    payload = {'image': {'image_bytes': content }}
    params = {}
    print("*"*30)
    res = prediction_client.predict(name, payload, params)
    print (res)
    print("*"*30)
    return res


ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg' }


@app.route('/malaria')
def malaria():
   return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename.split('.')[-1] in  ALLOWED_EXTENSIONS:
            pred = predict_malaria(file)
            res = {
                    'class':pred.payload[0].display_name,
                    'score':pred.payload[0].classification.score
            }
            print(res)
    return jsonify(res), 200
		
if __name__ == '__main__':
   app.run(debug = True)

