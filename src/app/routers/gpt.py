from fastapi import FastAPI
import logging
from extract_the_result import load_action_prompt
from extract_the_result import chat_with_prompt_for_pic
from extract_the_result import AiCmdEnum
import urllib.parse
import requests
import uvicorn
import config.constants as ct
import json


# 配置logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app2 = FastAPI(
    title="OpenAI微服务",
    version="0.1.0",
)


@app2.put("/gpt/")
async def gpt_llm(repid: str, chara: str):
    logger.info(f'成功接收chara！')
    # 将chara转回字典
    chara = json.loads(chara)
    final = []
    for i in chara.keys():
        final.append(chara[i])
    logger.info(final)

    logger.info(f'openAI start!')
    ocr_prompt = load_action_prompt(AiCmdEnum.orc)

    result = chat_with_prompt_for_pic(ocr_prompt, mode="gpt-3.5-turbo", temperature=0.0, content=final)
    results = {repid: result}
    logger.info(f'openAI ended')
    encoded_params = urllib.parse.urlencode(results)
    base_url = "https://127.0.0.1:29081/api/v1/reqhistory/item/?reqid={}&res={}".format(repid, encoded_params)

    response = requests.put(base_url, data=encoded_params, verify=False)

    if response.status_code == requests.codes.ok:
        print("PUT请求成功！")
    else:
        print("PUT请求失败！")
    return

@app2.put("/test/")
async def test(repid: str, chara: str):
    return repid, chara


if __name__ == '__main__':
    # 启动fastAPI
    uvicorn.run(app2,
                host='0.0.0.0',
                port=29082,
                ssl_keyfile=ct.SCHEDULE_KEY,
                ssl_certfile=ct.SCHEDULE_CER
                )
