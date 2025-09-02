from typing_extensions import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import os


class BlogState(TypedDict, total=False):
    messages: list
    topic: str
    outline: str
    key_points: str


MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


PROMPT = (
    "You are a meticulous research assistant. Given a blog topic, produce: \n"
    "1) A crisp one-paragraph context intro (non-fluffy).\n"
    "2) A hierarchical outline with 5-8 H2 sections and bullets.\n"
    "3) A bullet list of key facts/stats (no URLs).\n"
)


def researcher(state: BlogState) -> BlogState:
    topic = state.get("topic") or "AI Trends"
    llm = ChatGoogleGenerativeAI(model=MODEL, google_api_key=os.getenv("GOOGLE_API_KEY"))

    res = llm.invoke([
        HumanMessage(content=f"Topic: {topic}\n\n{PROMPT}")
    ])

    content = res.content if hasattr(res, "content") else str(res)
    outline = content
    key_points = content

    return {
        "messages": [res],
        "outline": outline,
        "key_points": key_points,
    }
