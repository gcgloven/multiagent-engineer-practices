"""Intentionally defective, fictional article-preview compiler.

This module returns in-memory HTML; it never writes or publishes files.
"""


class ArticleBundle:
    def __init__(self):
        self._pages = {}

    def replace_articles(self, articles):
        # Defect: partial mutation can destroy the previous valid preview.
        self._pages.clear()
        for article in articles:
            slug = article["slug"]
            title = article["title"]
            body = article["body"]
            if not title or not body:
                raise ValueError("Title and body are required")
            # Defects: path-like names and literal HTML are accepted.
            self._pages[f"{slug}.html"] = (
                f"<!doctype html><title>{title}</title><p>{body}</p>\n"
            )

    def snapshot(self):
        return dict(self._pages)
