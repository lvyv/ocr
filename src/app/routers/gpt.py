from fastapi import FastAPI, Depends
import logging
from extract_the_result import load_action_prompt
from extract_the_result import chat_with_prompt_for_pic
from extract_the_result import AiCmdEnum
# import urllib.parse
import requests
import uvicorn
import json
import os
from typing import List
from fastapi import File, UploadFile
import config.constants as ct
from app.services.reqhistory import ReqHistoryService
from config.database import get_db


os.environ['http_proxy'] = ct.OPEN_AI_HTTP_PROXY
os.environ['https_proxy'] = ct.OPEN_AI_HTTP_PROXY
# 配置logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app2 = FastAPI(
    title="OpenAI微服务",
    version="0.1.0",
)


@app2.put("/gpt/")
async def gpt_llm(repid: str, chara: str, db: get_db = Depends()):
    logger.info(f'成功接收chara！')
    # 将chara转回字典
    chara = json.loads(chara)
    final = []
    for i in chara.keys():
        final.append(chara[i])
    logger.info(final)

    logger.info(f'openAI start!')
    ocr_prompt = load_action_prompt(AiCmdEnum.orc)

    try:
        result = chat_with_prompt_for_pic(ocr_prompt, mode=ct.OPEN_AI_MODEL, temperature=0.0, content=final)

    except Exception as err:
        logger.error(err)
        result = 'OpenAI调用出现错误'

    logger.info(f'openAI ended')

    # 将结果保存入数据库
    logger.info(f'save db start!')
    reqs = ReqHistoryService(db)
    result = reqs.update_item(repid, result)
    logger.info(f'save db ended!')
    return result


@app2.post("/test/")
async def test(files: List[UploadFile] = File(...)):
    file_bytes = None
    for file in files:
        file_bytes = await file.read()
    img_files = [("files", file_bytes)]

    url = f"https://127.0.0.1:29083/ocr/"
    response = requests.post(url, files=img_files, verify=False)

    if response.status_code == requests.codes.ok:
        print("PUT请求成功！")
    else:
        print("PUT请求失败！")

    li_data = response.json()
    data = json.loads(li_data)
    return data


if __name__ == '__main__':
    # 启动fastAPI
    logger.info(f'*********************  GPT AI services  ********************')
    uvicorn.run(app2,
                host='0.0.0.0',
                port=29082,
                ssl_keyfile=ct.SCHEDULE_KEY,
                ssl_certfile=ct.SCHEDULE_CER
                )
