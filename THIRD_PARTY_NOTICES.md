# Third-party notices

This project adapts concepts from the following MIT-licensed reference works. The template wording is newly authored; these notices retain attribution for the reviewed sources.

The problem-framing method also credits Design Council's [Framework for Innovation](https://www.designcouncil.org.uk/resources/framework-for-innovation/) under the source's stated [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) terms. Its divergent/convergent thinking is explained and adapted in original wording; no source diagram is reproduced. External PDF skills and tools are linked in the documentation, not bundled, and retain their own terms.

## Skills For Real Engineers — Matt Pocock

Source: [upstream repository](https://github.com/mattpocock/skills) · [MIT license](https://github.com/mattpocock/skills/blob/main/LICENSE). Source and license checked 2026-11-02.

MIT License

Copyright (c) 2026 Matt Pocock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Multica Best Practices

Source: [upstream repository](https://github.com/it235/multica-best-practices) · [MIT license](https://github.com/it235/multica-best-practices/blob/main/LICENSE). Source and license checked 2026-11-02. The method-level mapping is documented in [docs/skill-design.md](docs/skill-design.md).

MIT License

Copyright (c) 2026 Multica Squad Playbook Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


## ub-mode and quality toolkits

The `ub-coding`, `ub-review` and `ub-design` methods are scoped adaptations informed by [unclebob/ub-mode](https://github.com/unclebob/ub-mode/tree/57a8bdd28e45ed41900ace0bafa2ff76dd9ed70f). The specific upstream [SKILL.md at that commit](https://github.com/unclebob/ub-mode/blob/57a8bdd28e45ed41900ace0bafa2ff76dd9ed70f/SKILL.md) is the evidence reference recorded in `toolkits.lock.json` and in each adapting skill.

**Disclaimer:** The upstream [`ub-mode` revision](https://github.com/unclebob/ub-mode/tree/57a8bdd28e45ed41900ace0bafa2ff76dd9ed70f) contains no `LICENSE` file. This is a disclosure of the source repository's licensing documentation; it does not grant permission or change the rights of the original author.

The optional host bootstrap fetches Crapper, Dryer and Mutator at the exact revisions in `toolkits.lock.json`. Their source checkouts retain their own Zero-Clause BSD license files under the installed environment's `sources` directory. Python dependencies retain their individual distribution licenses; they are installed from the pinned requirements, not copied into this repository's source. UML Viewer is referenced as an optional future integration and is not installed.
