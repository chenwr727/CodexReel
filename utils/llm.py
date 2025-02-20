from openai import OpenAI

from utils.log import logger


class LLmWriter:
    def __init__(self, api_key: str, base_url: str, model: str):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    async def writer(self, content: str, system_prompt: str, **kwargs) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ]
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                timeout=300,
                **kwargs,
            )
            if (
                response.choices
                and response.choices[0]
                and response.choices[0].message
                and response.choices[0].message.content
            ):
                return response.choices[0].message.content
            else:
                raise ValueError("Unexpected response format")
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return None
