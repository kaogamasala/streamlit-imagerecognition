import streamlit as st
import io
import requests
import json
from PIL import Image, ImageDraw

st.title('顔認識アプリ')

with open('secret.json') as f:
    secret_json = json.load(f)
    
subscription_key = secret_json['SUBSCRIPTION_KEY']
assert subscription_key

face_api_url =  'https://20210723kaogamasala.cognitiveservices.azure.com/face/v1.0/detect'

uploaded_file = st.file_uploader("Choose an Image...", type=['jpg','png'])
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue()
        
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': subscription_key
        }
        params = {
            'returnFaceId': 'true',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
        }
        res = requests.post(face_api_url, params=params, headers=headers, data=binary_img)

        fontpath = "RictyDiminished-Regular.ttf"
        font = ImageFont.truetype(fontpath, 80)

        results = res.json()
        for result in results:
            rect = result['faceRectangle']
            
            attri = result['faceAttributes']
            age = str(attri['age'])
            happiness_key = list(attri['emotion'].keys())[4]
            happiness_value = list(attri['emotion'].values())[4]
            happiness_value_str = str(happiness_value)
    
            draw = ImageDraw.Draw(img)
            draw.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width'],rect['top']+rect['height'])], fill=None, outline='green', width=10)
            draw.text((rect['left'], rect['top']-200), "性別:"+ attri['gender'], font=font,fill='red')
            draw.text((rect['left'], rect['top']-100), "年齢:"+ age, font=font,fill='red')
            draw.text((rect['left'], rect['top']-400), happiness_key+":", font=font,fill='red')
            draw.text((rect['left'], rect['top']-300), happiness_value_str, font=font,fill='red')

        st.image(img, caption='Uploaded Image.', use_column_width=True)