import requests
import yaml
from src.config.logging import logger


url = "https://api.siliconflow.cn/v1/chat/completions"
silicon_config_path = '.\\credentials\\silicon.yml'
with open(silicon_config_path, 'r') as f:
    silicon_config = yaml.safe_load(f)
    api_key = silicon_config['api_key']


def chat_silicon(messages, model="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"):
    headers = {
        "Authorization": "Bearer "+api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "max_tokens": 4096,
        "stop": None,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "frequency_penalty": 0.5,
        "n": 1,
        "response_format": {"type": "text"},
    }
    try:
        logger.debug("messages:\n", messages)
        logger.info(f"Generating response from {model}")
        response = requests.request("POST", url, json=payload, headers=headers)

        if not response.text:
            logger.error("Empty response from the model")
            return None

        logger.info("Successfully generated response")
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return None


if __name__ == '__main__':
    print(chat_silicon([
        {
            "role": "user",
            "content":"介绍一下Lambda-CDM模型"
        }
    ]))