from typing_extensions import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import os


class BlogState(TypedDict, total=False):
    messages: list
    topic: str
    outline: str
    key_points: str
    blog_markdown: str


MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


PROMPT = (
    "Write a comprehensive, well-structured Markdown blog post.\n"
    "Use engaging but concise language, avoid hype.\n"
    "Requirements:\n"
    "- Start with a compelling intro (2-3 sentences).\n"
    "- Use clear H2/H3, bullet lists, and short paragraphs.\n"
    "- Include practical takeaways and examples.\n"
    "- End with a short actionable conclusion.\n"
)


def writer(state: BlogState) -> BlogState:
    topic = state.get("topic", "AI Trends")
    outline = state.get("outline", "")
    points = state.get("key_points", "")

    llm = ChatGoogleGenerativeAI(model=MODEL, google_api_key=os.getenv("GOOGLE_API_KEY"))

    res = llm.invoke([
        HumanMessage(content=(
            f"Topic: {topic}\n\nOutline:\n{outline}\n\nKey points:\n{points}\n\n{PROMPT}"
        ))
    ])

    draft = res.content if hasattr(res, "content") else str(res)

    return {
        "messages": [res],
        "blog_markdown": draft,
    }
