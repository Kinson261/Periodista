from ollama import chat, ChatResponse, Client
import dotenv

URL = dotenv.get_key(".env", "OLLAMA_URL")

def summarize(doc):
    client = Client(
        host=URL
    )
    response = client.chat(model='llama3.1:8b',
                           messages=[
                               {
                                   'role': 'user',
                                   'content': 'summarize {}'.format(doc),
                               },
                           ])

    print(response.message.content)
