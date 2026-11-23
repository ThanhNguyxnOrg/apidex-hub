import json
import re
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = SCRIPTS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from parse_readme import update_readme_counts

SENTENCE = (
    "We maintain a curated catalog of **{apis}** public APIs across **{cats}** categories; "
    "**{endpoints}** of them {verb} a recorded API endpoint, and the rest link to official documentation."
)
SENTENCE_RE = re.compile(
    r"catalog of \*\*([\d,]+)\*\* public APIs across \*\*(\d+)\*\* categories; "
    r"\*\*([\d,]+)\*\* of them (?:has|have) a recorded API endpoint"
)


class ReadmeCountsTests(unittest.TestCase):
    def test_counts_and_verb_are_rewritten_from_data(self):
        old = SENTENCE.format(apis="4,239", cats=70, endpoints=1, verb="has")
        new = update_readme_counts(old, 5000, 71, 12)
        self.assertEqual(new, SENTENCE.format(apis="5,000", cats=71, endpoints=12, verb="have"))
        self.assertEqual(update_readme_counts(new, 5000, 71, 1), SENTENCE.format(apis="5,000", cats=71, endpoints=1, verb="has"))

    def test_readme_does_not_call_catalog_entries_endpoints(self):
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotRegex(readme, r"\*\*[\d,]+\*\* public endpoints")
        self.assertNotIn("collection of public endpoints", readme)

    def test_readme_counts_match_generated_data(self):
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        meta = json.loads((REPO_ROOT / "site/src/data/apis.json").read_text(encoding="utf-8"))["meta"]
        match = SENTENCE_RE.search(readme)
        self.assertIsNotNone(match, "README catalog sentence not found")
        apis, cats, endpoints = (int(g.replace(",", "")) for g in match.groups())
        self.assertEqual(apis, meta["total_apis"])
        self.assertEqual(cats, meta["total_categories"])
        self.assertEqual(endpoints, meta["api_endpoint_count"])


if __name__ == "__main__":
    unittest.main()
