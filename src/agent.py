import dotenv
import ollama

env = dotenv.dotenv_values()


class Agent:
    def __init__(self, local: bool = True, model: str = "Llama3.1:8b", role: str = "user", streaming: bool = False) -> None:
        self.local: bool = local
        self.model: str = model
        self.role: str = role
        self.streaming: bool = streaming
        if self.local:
            self.client = ollama.Client(host=env["OLLAMA_URL"])
            self.client_async = ollama.AsyncClient(host=env["OLLAMA_URL"])
        else:
            self.client = ollama.Client()
            self.client_async = ollama.AsyncClient()

    def is_available(self):
        try:
            ollama.Client(host=env["OLLAMA_URL"]).chat(self.model)
        except ollama.ResponseError as e:
            print(f"Error {e.status_code}: {e.error}")
            return False
        return True

    def pull_model(self):
        try:
            ollama.Client(host=env["OLLAMA_URL"]).pull(self.model)
        except Exception as e:
            print(f"Something went wrong: {type(e).__name__} - {e}")

    def list_model(self):
        try:
            ollama.Client(host=env["OLLAMA_URL"]).list()
        except Exception as e:
            print(f"Something went wrong: {type(e).__name__} - {e}")

    def local_agent(self, prompt: str):
        if self.streaming:
            response = self.client.chat(
                model=self.model,
                messages=[{"role": self.role, "content": prompt}],
                stream=True,
            )
            for chunk in response:
                print(chunk["message"]["content"], end="", flush=True)
        else:
            response = self.client.chat(model=self.model, messages=[{"role": self.role, "content": prompt}])
            print(response.message.content)

    async def chat(self, prompt: str):
        message = {"role": "user", "content": prompt}
        if self.streaming:
            async for part in await self.client_async.chat(model=self.model, messages=[message], stream=True):
                print(part["message"]["content"], end="", flush=True)
        else:
            response = await self.client_async.chat(model=self.model, messages=[message])
            print(response.message.content)


if __name__ == "__main__":
    agent = Agent(local=True, model=env["OLLAMA_MODEL"], role="User", streaming=True)
    agent.local_agent("Hello, how are you?")
