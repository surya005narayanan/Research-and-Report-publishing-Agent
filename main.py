from typing import Annotated, Optional, Dict, Any
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os

from agents.researcher import researcher
from agents.writer import writer
from agents.seo import seo_optimizer
from agents.publisher import maybe_publish
from utils.io import save_markdown

load_dotenv()

class BlogState(TypedDict, total=False):
    messages: Annotated[list, add_messages]
    topic: str
    outline: str
    key_points: str
    blog_markdown: str
    seo: Dict[str, Any]
    published_url: Optional[str]

graph = StateGraph(BlogState)

graph.add_node("researcher", researcher)
graph.add_node("writer", writer)
graph.add_node("seo", seo_optimizer)
graph.add_node("publisher", maybe_publish)

graph.set_entry_point("researcher")
graph.add_edge("researcher", "writer")
graph.add_edge("writer", "seo")
graph.add_edge("seo", "publisher")

app = graph.compile()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Research → Write → SEO → Publish")
    parser.add_argument("topic", type=str, help="Topic to blog about (quoted)")
    parser.add_argument("--save", action="store_true", help="Save markdown locally")
    args = parser.parse_args()

    initial_state: BlogState = {
        "messages": [],
        "topic": args.topic,
    }

    state = app.invoke(initial_state)

    print("\n=== 📄 Blog Draft (Markdown) ===\n")
    print(state.get("blog_markdown", "<no draft>"))

    if args.save or not state.get("published_url"):
        path = save_markdown(state.get("blog_markdown", ""), state.get("seo", {}))
        print(f"\n💾 Saved to: {path}")

    if state.get("seo"):
        print("\n=== 🔍 SEO Suggestions ===")
        for k, v in state["seo"].items():
            print(f"- {k}: {v}")

    if state.get("published_url"):
        print(f"\n✅ Published: {state['published_url']}")
    else:
        print("\nℹ️ Not published (missing Medium credentials or error). Kept local copy.")
