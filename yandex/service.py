import openai

from django.conf import settings


class GPTError(Exception):
    pass


class YandexGpt():
    def __init__(self, api_key, folder_key):
        self.API_KEY = api_key
        self.CATALOG_KEY = folder_key

        self._init_client()

    def _init_client(self):
        self.client = openai.OpenAI(
            api_key=self.API_KEY,
            base_url="https://rest-assistant.api.cloud.yandex.net/v1",
            project=self.CATALOG_KEY
        )

    def get_reponse(self, input: str, instructions: str, temerature=1.0):

        response = self.client.responses.create(
            model=f"gpt://{self.CATALOG_KEY}/yandexgpt",
            input=input,
            instructions=instructions,
            temperature=temerature
        )
        print(response)
        return response.output[0].content[0].text

    def get_association(self, word: str, exclude: str = ""):
        
        prompt = f"Отвечай только одним или двумя словами. Придумай необычную ассоциацию к слову. Не повторяйся. Вот что уже было: {exclude}"
        word = self.get_reponse(input=word, instructions=prompt)
        
        if not word:
            raise GPTError('Пустой ответ от нейросети')
        if len(word.split(' ')) > 3:
            raise GPTError(f'Слишком много слов в ответе {word}')
        
        return word
    
    

if __name__ == "__main__":
    import os 
    from dotenv import load_dotenv
    load_dotenv()

    yandex = YandexGpt(os.getenv('YANDEX_API_KEY'), os.getenv('YANDEX_CATALOG'))
    word = yandex.get_association('подорожник')
    print(word)


