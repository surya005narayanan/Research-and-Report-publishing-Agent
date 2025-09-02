# publisher.py
from typing_extensions import TypedDict
from typing import Dict, Any, Optional
import os
import base64
import requests

def _require_env(key: str) -> str:
    v = os.getenv(key)
    if not v:
        raise ValueError(f"Missing env: {key}")
    return v

def _wp_auth_headers() -> Dict[str, str]:
    username = os.getenv("WP_USERNAME")
    app_password = os.getenv("WP_APP_PASSWORD")  
    jwt = os.getenv("WP_JWT_TOKEN")

    if username and app_password:
        token = base64.b64encode(f"{username}:{app_password}".encode("utf-8")).decode("ascii")
        return {"Authorization": f"Basic {token}"}
    if jwt:
        return {"Authorization": f"Bearer {jwt}"}
    return {}

def _publish_to_wordpress(md: str, seo: Dict[str, Any]) -> Optional[str]:
    site = os.getenv("WP_SITE_URL")  # e.g., https://example.com
    if not site:
        return None

    # Build headers
    headers = {
        "Content-Type": "application/json",
        **_wp_auth_headers(),
    }
    if "Authorization" not in headers:
        # No credentials available
        return None

    title = (seo.get("title") or "Untitled")[:65]
    slug = seo.get("slug") or ""
    excerpt = seo.get("excerpt") or ""
    content = md

    payload: Dict[str, Any] = {
        "title": title,
        "content": content,
        "status": os.getenv("WP_POST_STATUS", "publish"),  # publish | draft | pending
    }
    if slug:
        payload["slug"] = slug
    if excerpt:
        payload["excerpt"] = excerpt
    url = f"{site.rstrip('/')}/wp-json/wp/v2/posts"
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
    except Exception:
        return None

    if 200 <= resp.status_code < 300:
        data = resp.json()
        # The REST API returns link (permalink) for the created post
        return data.get("link") or data.get("guid", {}).get("rendered")
    else:
        try:
            print("WordPress publish error:", resp.status_code, resp.text)
        except Exception:
            pass
        return None

def maybe_publish(state: "BlogState") -> "BlogState":
    md = state.get("blog_markdown", "")
    seo = state.get("seo", {})
    if not md:
        return state
    url = _publish_to_wordpress(md, seo)
    if url:
        return {"published_url": url}
    return {}
