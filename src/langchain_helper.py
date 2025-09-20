import os
from urllib import response
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import wikipedia


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

# Convert into Langchain tool

def ask_text(question:str) -> str:
    """
    Ask a question to the LLM.
    Args:
        question (str): The question to ask.
    """
    llm, prompt_template = set_up(
        model='deepseek/deepseek-r1:free',
        input_vars=["text"],
        prompt="{text}"
    )
    chain = prompt_template | llm
    response = chain.invoke({"text": question})
    return response.content

# Convert into Langchain tool
def search_text(query: str) -> str:
    """
    Search for a query using DuckDuckGo.
    Args:
        query (str): The query to search for.
    """
    llm, prompt_template = set_up(
        model='deepseek/deepseek-r1:free',
        input_vars=["query"],
        prompt="Extract the topic as a Wikipedia topic from the following query: {query}. Respond with just the topic name with no fonts, just plain text."
    )
    print("HEY")
    chain = prompt_template | llm
    response = chain.invoke({"query": query})
    print(response.content)
    results = wikipedia.search(response.content)
    print(f"Wiki result: {results[0]}")
    # summary, content, links
    summary = wikipedia.summary(results[0], sentences=3)
    full_body = wikipedia.page(results[0]).content
    links = wikipedia.page(results[0]).links
    if not summary:
        return "No results found."
    else:
        llm, prompt_template = set_up(
            model='deepseek/deepseek-r1:free',
            input_vars=["summary", "content", "links", "topic", "query"],
            prompt="""Here is the summary about {topic}: {summary}. 
            Extract an answer to the question: {query} based on the content.
            Also, provide relevant links at the end of your response: {links}"""
        )
        chain = prompt_template | llm
        response = chain.invoke({
            "summary": summary,
            "content": full_body,
            "links": ', '.join(links[:5]),
            "topic": results[0],
            "query": query
        })
        return response.content

    
def main():
    print(search_text("Who is the president of the united states?"))
    models = {
        'text': "deepseek/deepseek-r1:free",
        'audio': "deepseek/deepseek-a1:free",
        'image': "deepseek/deepseek-i1:free"
    }

if __name__ == "__main__":
    main()