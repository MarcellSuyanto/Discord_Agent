import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
   """Multiply two numbers."""
   return a * b



def set_up(model:str, input_vars:str, prompt:str) -> tuple[ChatOpenAI, PromptTemplate]:
    """
    Set up the LLM and prompt template.
    Args:
        model (str): The model to use.
        input_vars (str): The input variables for the prompt template.
        prompt (str): The prompt template.
    """

    load_dotenv()
    API_KEY = os.getenv("OPENROUTER_KEY")
    llm = ChatOpenAI(
        model=model,
        base_url="https://openrouter.ai/api/v1",
        temperature=0.7,
        api_key=API_KEY
    )

    prompt_template = PromptTemplate(
        input_variables=input_vars,
        template=prompt
    )

    return llm, prompt_template


def main():

    models = {
        'text': "deepseek/deepseek-r1:free",
        'audio': "deepseek/deepseek-a1:free",
        'image': "deepseek/deepseek-i1:free"
    }

    llm, prompt_template = set_up(
        model=models['text'],
        input_vars=["text"],
        prompt="What is {text}?"
    )
    chain = prompt_template | llm
    response = chain.invoke({"text": "Retrieval Augmented Generation"})
    print(response.content)

