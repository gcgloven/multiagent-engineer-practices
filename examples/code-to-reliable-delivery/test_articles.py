"""Behavior checks for a fictional in-memory article-preview compiler."""

import unittest

from articles import ArticleBundle
from before import ArticleBundle as BeforeBundle


def article(slug="garden-notes", title="Garden notes", body="A story about a garden."):
    return {"slug": slug, "title": title, "body": body}


class BaselineReproduction(unittest.TestCase):
    def test_path_like_slug_becomes_an_output_name(self):
        bundle = BeforeBundle()
        bundle.replace_articles([article(slug="../outside")])
        self.assertIn("../outside.html", bundle.snapshot())

    def test_plain_text_is_interpreted_as_html(self):
        bundle = BeforeBundle()
        bundle.replace_articles([article(body="<script>unexpected()</script>")])
        self.assertIn("<script>", bundle.snapshot()["garden-notes.html"])

    def test_invalid_replacement_discards_previous_preview(self):
        bundle = BeforeBundle()
        bundle.replace_articles([article(slug="old")])
        with self.assertRaises(ValueError):
            bundle.replace_articles([article(slug="new"), article(slug="broken", body="")])
        self.assertEqual(set(bundle.snapshot()), {"new.html"})


class CandidateContract(unittest.TestCase):
    def test_valid_replacement_contains_only_the_new_articles(self):
        bundle = ArticleBundle()
        bundle.replace_articles([article(slug="old")])
        bundle.replace_articles([article(slug="chapter-1"), article(slug="chapter-2")])
        self.assertEqual(set(bundle.snapshot()), {"chapter-1.html", "chapter-2.html"})
        self.assertIn('<meta charset="utf-8">', bundle.snapshot()["chapter-1.html"])

    def test_title_and_body_are_escaped_and_unicode_is_preserved(self):
        bundle = ArticleBundle()
        bundle.replace_articles([article(title='A < B & "C"', body="Café <script>x()</script>")])
        rendered = bundle.snapshot()["garden-notes.html"]
        self.assertIn("<title>A &lt; B &amp; &quot;C&quot;</title>", rendered)
        self.assertIn("Café &lt;script&gt;x()&lt;/script&gt;", rendered)
        self.assertNotIn("<script>", rendered)

    def test_invalid_slugs_are_rejected(self):
        for slug in ("../outside", "/absolute", "a/b", "a\\b", "Upper", "two words", "", "a..b", "-start", "end-", "a--b", "café", None, 7):
            with self.subTest(slug=slug), self.assertRaises(ValueError):
                ArticleBundle().replace_articles([article(slug=slug)])

    def test_duplicate_names_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate slug"):
            ArticleBundle().replace_articles([article(), article(title="Another title")])

    def test_invalid_record_shapes_and_text_are_rejected(self):
        invalid = [None, [], {}, {"slug": "a", "title": "A"}, dict(article(), extra="x")]
        for field in ("title", "body"):
            for value in ("", " \n", None, 0):
                invalid.append(dict(article(), **{field: value}))
        for record in invalid:
            with self.subTest(record=record), self.assertRaises(ValueError):
                ArticleBundle().replace_articles([record])

    def test_failed_replacement_preserves_the_entire_previous_preview(self):
        bundle = ArticleBundle()
        bundle.replace_articles([article(slug="old")])
        previous = bundle.snapshot()
        for invalid in (article(body=""), article(slug="../outside"), article(slug="new")):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                bundle.replace_articles([article(slug="new"), invalid])
            self.assertEqual(bundle.snapshot(), previous)

    def test_input_iteration_failure_preserves_the_previous_preview(self):
        def interrupted_input():
            yield article(slug="new")
            raise RuntimeError("Input stopped")

        bundle = ArticleBundle()
        bundle.replace_articles([article(slug="old")])
        previous = bundle.snapshot()
        with self.assertRaisesRegex(RuntimeError, "Input stopped"):
            bundle.replace_articles(interrupted_input())
        self.assertEqual(bundle.snapshot(), previous)

    def test_input_and_snapshot_mutation_do_not_change_the_preview(self):
        bundle = ArticleBundle()
        original = article()
        bundle.replace_articles([original])
        previous = bundle.snapshot()
        original["body"] = "Changed after rendering"
        returned = bundle.snapshot()
        returned.clear()
        self.assertEqual(bundle.snapshot(), previous)

    def test_empty_input_deliberately_clears_the_preview(self):
        bundle = ArticleBundle()
        bundle.replace_articles([article()])
        bundle.replace_articles([])
        self.assertEqual(bundle.snapshot(), {})


if __name__ == "__main__":
    unittest.main()
