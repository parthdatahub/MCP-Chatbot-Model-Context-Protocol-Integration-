import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("API_KEY"),
    api_version="2023-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

deployment_name = os.getenv("DEPLOYMENT_NAME")

def ask_gpt(question, context="", source="email"):
    """
    Ask GPT using Azure OpenAI with source-specific prompt.

    :param question: The user question
    :param context: Text context (email or file)
    :param source: "email" or "file" (default: email)
    :return: GPT response string
    """
    system_prompt = {
        "email": "You are an assistant that answers based on Outlook emails.",
        "file": "You are a helpful assistant answering questions from uploaded or cloud-based documents.",
        "teams": "You are an assistant that answers based on Microsoft Teams messages."
    }.get(source, "You are a helpful assistant.")

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ],
        temperature=0.4,
        max_tokens=500
    )

    return response.choices[0].message.content
