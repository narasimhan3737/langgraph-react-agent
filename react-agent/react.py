from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

@tool
def triple(num:float) -> float:
    """
    :param num: a number to triple
    :return: the number tripled ->  multiplied by 3
    """
    return float(num) * 3

tools = [TavilySearch(max_results=1), triple]

#llm = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash").bind_tools(tools)

