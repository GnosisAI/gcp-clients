from flask import Flask, render_template, request, jsonify
from google.cloud import automl_v1beta1

#* Global vars
model_id = "ICN2708198090334566848"
project_id = "unified-skein-232719"
name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
prediction_client = automl_v1beta1.PredictionServiceClient()

app = Flask(__name__) 

def predict_malaria(file):

    content = file.read()
    payload = {'image': {'image_bytes': content }}
    params = {}
    res = prediction_client.predict(name, payload, params)
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

