from typing import Dict, Any
from typing_extensions import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import re
import os


class BlogState(TypedDict, total=False):
    messages: list
    blog_markdown: str
    seo: Dict[str, Any]


MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


PROMPT = (
    "You are an SEO assistant. Given a markdown article, return:\n"
    "- title (<= 65 chars)\n- slug (kebab-case)\n"
    "- meta_description (<= 155 chars)\n- keywords (comma list, <=8)\n"
    "- hashtags (<=6, with #)\n- excerpt (1-2 sentences)\n"
    "Return as clear labeled lines."
)


def kebab(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s).strip("-")
    return s


def seo_optimizer(state: BlogState) -> BlogState:
    article = state.get("blog_markdown", "")
    llm = ChatGoogleGenerativeAI(model=MODEL, google_api_key=os.getenv("GOOGLE_API_KEY"))

    res = llm.invoke([HumanMessage(content=f"{PROMPT}\n\nARTICLE:\n{article}")])
    text = res.content if hasattr(res, "content") else str(res)

    # Simple parse
    def grab(label):
        m = re.search(rf"{label}\s*:\s*(.*)", text, flags=re.IGNORECASE)
        return m.group(1).strip() if m else ""

    title = grab("title") or "Untitled Blog"
    data = {
        "title": title[:65],
        "slug": kebab(grab("slug") or title),
        "meta_description": grab("meta_description")[:155],
        "keywords": grab("keywords"),
        "hashtags": grab("hashtags"),
        "excerpt": grab("excerpt"),
    }

    return {"messages": [res], "seo": data}
