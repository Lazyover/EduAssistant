from openai import OpenAI

from src.config.logging import logger


def chat_lm_studio(messages):
    try:
        logger.debug("messages:\n", messages[0]['content'])
        logger.info("Generating response from Gemini")
        client = OpenAI(api_key="lm-studio", base_url="http://127.0.0.1:1234/v1")

        response = client.chat.completions.create(
            model="meta-llama-3.1-8b-instruct",
            messages=messages,
            stream=False
        )

        if not response.choices[0].message.content:
            logger.error("Empty response from the model")
            return None

        logger.info("Successfully generated response")
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return None