from fastapi import FastAPI
from pydantic import BaseModel
import qrcode
from PIL import Image
import io
import qrcode.constants
import requests
import base64

app = FastAPI()

class QRCode(BaseModel):
    data: str
    logo: str

@app.post("/qr/")
def generate_qrcode(request: QRCode):
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    qr.add_data(request.data)
    img = qr.make_image().convert("RGBA")

    #get logo
    res = requests.get(request.logo)
    logo_data = res.content
    logo = Image.open(io.BytesIO(logo_data)).convert('RGBA')
    logo.thumbnail([img.width/4.5, img.height/4.5], Image.Resampling.LANCZOS)
    
    img.paste(logo, [int(img.width/2 - logo.width/2), int(img.height/2 - logo.height/2)])
    
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='PNG')
    img_data = img_byte_array.getvalue()
    
    return {
        "qrcode": f"data:image/png;base64,{base64.b64encode(img_data).decode()}"
    }
