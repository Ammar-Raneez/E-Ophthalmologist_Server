import numpy as np
import azure.functions as func
import json
import uuid
from .app import upload
from azure.storage.blob import BlobServiceClient, BlobClient, ContentSettings

def main(req: func.HttpRequest) -> func.HttpResponse:
    headers = {
        "Content-type": "application/json",
        "Access-Control-Allow-Origin": "*"
    }

    f = req.files['file']
    filename = str(uuid.uuid4()) + ".jpg"
    filestream = f.stream
    filestream.seek(0)

    # save image to azure storage blob
    try:
        blob = BlobClient.from_connection_string(conn_str= "DefaultEndpointsProtocol=https;AccountName=bisfyp;AccountKey=JQQqkIny5I6g73O9tg4wMUTSh3AYh7XwEhphLRWPKJJ3tZaW5J+LUHD0rM8n8+BLdwXmRijCKpAu40yyt2x2kA==", container_name="images", blob_name=filename)
        cnt_settings = ContentSettings(content_type="image/jpeg")
        blob.upload_blob(filestream.read(), blob_type="BlockBlob", content_settings=cnt_settings)
    except:                                                                                                                                                                          
        pass

    blob_data = blob.download_blob()
    x = blob_data.content_as_bytes()
    x = np.fromstring(x, dtype='uint8')
    results = upload(x)
    return func.HttpResponse(json.dumps([{"result": results, "image_url": f"https://bisfyp.blob.core.windows.net/images/{filename}"}]), headers = headers)

