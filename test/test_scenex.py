import os
import json
import base64
import requests
import datetime


def image_to_data_uri(file_path):
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded_image}"


if __name__ == '__main__':
    starttime = datetime.datetime.now()

    os.environ['http_proxy'] = 'http://127.0.0.1:49777'
    os.environ['https_proxy'] = 'http://127.0.0.1:49777'
    YOUR_GENERATED_SECRET = "Pu2NBWEpObJTHa7MvNeu:6d835129daf160d2feed9eea120dd3891d96305ae726d96fc63aadbc416b8c83"
    local_image_path = "E:/桌面/week/new/ocr/pic/F5.png"
    data = {
        "data": [
            {"image": "https://raw.githubusercontent.com/lvyv/ocr/yxl/pic/B10.png", "features": []},
            # {"image": image_to_data_uri(local_image_path), "features": []},
        ]
    }
    headers = {
        "x-api-key": f"token {YOUR_GENERATED_SECRET}",
        "content-type": "application/json",
    }
    data_bytes = json.dumps(data)
    api_url = "https://api.scenex.jina.ai/v1/describe"
    response = requests.post(api_url, data=data_bytes, headers=headers, timeout=(120, 120))   # 连接超时和读取超时
    txt = response.json()
    jstr = json.dumps(txt)
    print('------------------------------------------------')
    print(jstr)
    print('------------------------------------------------')
    endtime = datetime.datetime.now()
    print((endtime - starttime).seconds)
