"""Fictional offline article previews, produced entirely in memory.

The path labels are output names, not permission to write files. This module
has no filesystem, network, persistence, or website deployment behavior.
"""

from html import escape
import re


_SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
_FIELDS = frozenset(("slug", "title", "body"))


class ArticleBundle:
    def __init__(self):
        self._pages = {}

    def replace_articles(self, articles):
        """Replace the preview only after the complete input has been checked.

        Articles have exactly three string fields: slug, title, and body.
        Slugs contain lowercase ASCII letters/digits separated by hyphens.
        Title and body are plain text, with non-whitespace content.
        Empty input deliberately produces an empty bundle. Duplicate names
        are rejected. If input iteration or validation fails, the previous
        bundle remains available.
        """
        candidate = {}
        for article in articles:
            if not isinstance(article, dict) or article.keys() != _FIELDS:
                raise ValueError("Each article requires exactly slug, title, and body")
            slug, title, body = (article[key] for key in ("slug", "title", "body"))
            if not isinstance(slug, str) or _SLUG.fullmatch(slug) is None:
                raise ValueError("Slug must be lowercase words or digits joined by hyphens")
            if any(not isinstance(value, str) or not value.strip() for value in (title, body)):
                raise ValueError("Title and body must be nonempty plain text")
            filename = f"{slug}.html"
            if filename in candidate:
                raise ValueError(f"Duplicate slug: {slug}")
            safe_title, safe_body = escape(title), escape(body)
            candidate[filename] = (
                '<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
                f"<title>{safe_title}</title></head><body>"
                f"<h1>{safe_title}</h1><p>{safe_body}</p></body></html>\n"
            )
        self._pages = candidate

    def snapshot(self):
        """Return a detached mapping of output names to rendered HTML."""
        return dict(self._pages)
