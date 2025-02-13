import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

endpoint = "https://models.inference.ai.azure.com"
model_name = "o1"


token = os.getenv("GITHUB_TOKEN")
client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
    api_version="2024-12-01-preview",
)

response = client.complete(
    messages=[
        {
            "role": "developer",
            "content": "You are a helpful assistant.",
        },
        UserMessage(content="What is the capital of France?"),
    ],
    model=model_name
)

print(response.choices[0].message.content)