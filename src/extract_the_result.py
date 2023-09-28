from enum import Enum
import configparser        # 读取配置文件
import pathlib
from langchain.prompts import ChatPromptTemplate
from langchain import LLMChain
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
import config.constants as ct


class AiCmdEnum(str, Enum):
    """
        description: Ai command enum.
    """
    orc = 'orc'


def get_prompt_file_path(action: AiCmdEnum) -> str:           # 得到对应action的prompt文件路径
    env_obj = pathlib.Path(__file__)
    file_format = "{}_prompt.txt"
    file_name = file_format.format(action.value)
    prompt_file_path = env_obj.parent.parent.joinpath(f"prompts/{file_name}")
    # if prompt file does not exist, use default prompt.
    if not prompt_file_path.exists():
        prompt_file_path = env_obj.parent.parent.joinpath(f"prompts/default_prompt.txt")

    return str(prompt_file_path)


def load_prompt_from_file(filename) -> list:
    # read ini file.
    config = configparser.ConfigParser()
    config.read(filename, encoding="utf-8")

    # chat list.
    chat_list = []

    for section in config.sections():
        for option in config.options(section):
            value = config[section][option]
            chat_list.append((option, value))
    return chat_list


def load_action_prompt(action: AiCmdEnum) -> list:
    return load_prompt_from_file(get_prompt_file_path(action))


def chat_with_prompt_for_pic(template: list, mode: str, temperature: float, content: list) -> (
        list):
    """
    chat with prompt.
    :param template: chat prompt list.
    :param mode: chat model.
    :param temperature: chat temperature.
    :param content: extra value.
    :return: (result)
    """
    # 0.construct chat prompt.
    chat_template = ChatPromptTemplate.from_messages(template)
    # 1.init chat llm.
    llm = ChatOpenAI(temperature=temperature, model=mode, openai_api_key=ct.OPEN_AI_KEY,
                     openai_organization=ct.OPEN_AI_ORG)
    # 3.init llm chain
    chain = LLMChain(llm=llm, prompt=chat_template)
    # 4.generate response.

    result = chain.run(content)

    return result


if __name__ == "__main__":
    orc_prompt = load_action_prompt(AiCmdEnum.orc)
    print(orc_prompt)
