# C. Existing code → reliable delivery

This fictional example follows an offline article-preview compiler from a reported formatting problem to a reviewable candidate. The local Python fixture builds a mapping of output names to HTML strings. It never writes files, opens a browser, or publishes a website. All article content is invented for this example.

## Understand the reported problem

A small writing application previews a collection of plain-text articles. A title containing `<` renders incorrectly. Investigation reveals two more defects: article names can look like paths, and a failed replacement leaves a partially updated preview instead of the last valid collection.

The first request might be “fix the title formatting.” The engineer examines the complete boundary: article records → validation → HTML rendering → replacement of the preview collection. The problem includes interpretation of plain text and consistency after failure, so a visual patch alone would leave two observable defects unresolved.

The [baseline](code-to-reliable-delivery/before.py) reproduces three problems:

1. A name such as `../outside` becomes an output label. No file is written here, but the label is unsuitable for a future export boundary.
2. Literal HTML in an article is inserted into the page instead of displayed as text.
3. A malformed article encountered during replacement discards the old preview and leaves only the earlier records from the failed replacement.

A direct assignment to an engineer is suitable for investigation. A lead coordinates when another specialist or independent verifier enters. A design decision does not automatically require another agent.

## Frame the need and explore the design

**G-1:** Let a writer preview a complete collection of plain-text articles, with predictable names and no loss of the last valid preview when replacement fails.

The engineer establishes that the input contract is plain text, not rich HTML or Markdown. Treating the input as plain text makes escaping correct; a rich-text feature would need a separate content policy and implementation. The preview is deliberately an in-memory artifact. Safe file export, browser integration, persistence, and website publication are outside this fixture's verified scope.

Compare credible alternatives:

| Option | Assessment |
| --- | --- |
| Escape only the displayed title | Resolves the first visible symptom but leaves body interpretation and partial replacement unresolved. |
| Validate and render the complete candidate before replacing the preview | Fits the existing responsibility; makes plain-text handling, duplicate names, and failure behavior explicit. |
| Adopt a document parser and template system | Useful when rich authoring, themes, or extension points are required. Those needs would change the design and its verification scope. |

**ADR-1:** Keep the `replace_articles` and `snapshot` interface. Validate every record and prepare the complete replacement in a separate mapping; replace the current preview only when preparation succeeds. Escape title and body as HTML text. Reject ambiguous names and duplicates instead of silently rewriting or overwriting them.

This choice follows the current content contract. If writers require rich text, the third option becomes relevant; preserving the smallest implementation is not a reason to reject a supported requirement.

## Define behavior and acceptance

- **BR-1:** Each article has exactly `slug`, `title`, and `body` string fields. Title and body contain non-whitespace text.
- **BR-2:** A slug contains lowercase ASCII letters or digits, with single hyphens between groups. Names are unique within a collection.
- **BR-3:** Title and body are plain text and are escaped when rendered into HTML.
- **BR-4:** A failed input iteration or validation leaves the complete previous preview unchanged. Empty input deliberately replaces it with an empty collection.
**BR-5:** Changing input records or a returned snapshot after rendering cannot change the stored preview.

| Criterion | Observable check |
| --- | --- |
| **AC-1:** A successful replacement contains exactly the new collection. | Replace an old article with two new articles; only the two new names remain. |
| **AC-2:** Text remains text. | Render punctuation, Unicode, and a script-like string; special characters are escaped and the Unicode content remains present. |
| **AC-3:** Invalid or conflicting names do not enter the collection. | Reject paths, uppercase names, spaces, malformed hyphens, invalid types, and duplicate slugs. |
| **AC-4:** Failed replacement does not discard a valid preview. | Introduce a bad later record or an input-iteration exception; compare the full preview with its previous value. |
| **AC-5:** Input and output boundaries are explicit. | Reject invalid record shapes and empty content; check mutation isolation and deliberate empty replacement. |

These checks establish the in-memory contract. Output labels are not a filesystem security boundary: a later exporter must establish its own destination, overwrite, symbolic-link, and platform filename behavior before writing anything.

## Implement in useful increments

First reproduce the formatting error and state the content contract. Then add validation and escaped rendering. Finally stage the complete candidate before replacement and test failure after a valid first record, because checking only a bad first record would miss partial-update behavior.

The [candidate](code-to-reliable-delivery/articles.py) keeps validation and rendering in a single readable boundary. It does not introduce a framework merely to coordinate these operations. The same article contract can later support an editor adapter, but that integration will require evidence about its own behavior.

Run the local demonstration from the repository root:

```bash
python3 -B -m unittest discover -s examples/code-to-reliable-delivery -p 'test_*.py' -v
```

The [tests](code-to-reliable-delivery/test_articles.py) separate three baseline reproductions from nine candidate contract checks. Baseline tests intentionally confirm the known defects; their passing status does not mean the baseline is correct. Candidate tests assert rendered content, accepted names, rejected inputs, complete replacement, and failure preservation.

## Independent review and the leader's loop

For substantive code work, the engineer returns the exact candidate, criteria, contract changes, test command/results, and remaining limitations. The lead asks a qualified verifier to examine plain-text interpretation, failure behavior, compatibility impact, and the proposed target. The verifier can challenge assumptions and add adversarial cases rather than only rerun the author's suite.

For example, a verifier could find that the actual editor supplies rich text, or that empty replacement is an accidental destructive action in its interface. That finding should identify the violated criterion or disputed contract, evidence, and closure check. The engineer repairs the implementation or revisits the design; the verifier checks the result and affected regressions.

Two unsuccessful repair-and-verification rounds on the same problem stop the repeated approach. A materially different approach may proceed within scope and budget; failure history remains visible. Ordinary edit/test work and productive design exploration do not consume that repair counter.

This describes the intended agent workflow. The fixture has not been run through a live Multica squad. Passing local tests does not establish independent agent review.

## Grow readiness to the intended environment

| Intended use | Evidence needed beyond this fixture |
| --- | --- |
| Local preview library | Confirm the caller's content contract, supported Python version, error handling, integration tests, and user-facing explanation of rejected input. |
| Integrated writing application | Exercise actual editor input and browser rendering, accessibility, empty-replacement confirmation, recovery after errors, compatibility, and a rollback path. Decide how previews survive application restarts. |
| Public website delivery | Design and test export destination controls, supported filenames, permissions, overwrite behavior, publication authorization, deployment rollback, and applicable content handling. Exercise the full publishing journey before release. |

These are distinct acceptance boundaries. A request for public delivery requires the missing publication behavior and its evidence; an in-memory preview does not satisfy it. Revisiting architecture when requirements expand is part of the engineering process.

## What has actually been checked

The fictional baseline and candidate were executed locally with the command above: **12 tests passed** (3 defect reproductions and 9 candidate checks). No file export, browser rendering, website publication, persistent recovery, or Multica execution was verified. The workflow's independent review and release stages remain a worked procedure, not completed live gates.
