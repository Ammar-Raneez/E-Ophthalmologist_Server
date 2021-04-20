# import logging
import os
import numpy as np
import azure.functions as func
import cv2
import json
import uuid
from .app import upload
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient, BlobClient, ContentSettings

def main(req: func.HttpRequest) -> func.HttpResponse:
    headers = {
        "Content-type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }

    text_test = req.params.get("name")

    f = req.files['file']
    filename = str(uuid.uuid4()) + ".jpg"
    filestream = f.stream
    filestream.seek(0)

    # save image to azure storage blob
    try:
        blob = BlobClient.from_connection_string(conn_str= "DefaultEndpointsProtocol=https;AccountName=bisfyp;AccountKey=+NYIa2OlyIc/sPLMSeaSeWWU70o2CD8YX128gdbyG184M7F2EDuRDmilCmYOIowk/9/GmioI2FiE0hE+N9atnw==", container_name="images", blob_name=filename)
        cnt_settings = ContentSettings(content_type="image/jpeg")
        blob.upload_blob(filestream.read(), blob_type="BlockBlob", content_settings=cnt_settings)
    except:                                                                                                                                                                          
        pass

    if text_test:
        return func.HttpResponse(json.dumps("Hello, " + text_test), headers = headers)
    else:
        blob_data = blob.download_blob()
        x = blob_data.content_as_bytes()
        x = np.fromstring(x, dtype='uint8')
        results = upload(x)
        return func.HttpResponse(json.dumps([{"result": results, "image_url": f"https://bisfyp.blob.core.windows.net/images/{filename}"}]), headers = headers)
