from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class LegalPage(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.anchors = []
        self.scripts = 0
        self.sections = {}
        self.current = None
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and attrs.get('href', '').startswith('#'):
            self.anchors.append(attrs['href'][1:])
        if tag == 'script':
            self.scripts += 1
        if tag == 'section':
            self.current = attrs['id']
            self.sections[self.current] = ''

    def handle_endtag(self, tag):
        if tag == 'section':
            self.current = None

    def handle_data(self, data):
        if self.current:
            self.sections[self.current] += data


class LegalTest(unittest.TestCase):
    def test_downloads_and_html_match_the_reviewed_legal_export(self):
        documents = json.loads((ROOT / 'legal/documents.json').read_text())
        self.assertEqual({'terms', 'privacy'}, set(documents))
        for kind, doc in documents.items():
            expected = '\n\n'.join([doc['title'], f'Version {doc["version"]} · {doc["updated"]}'] +
                                   [value for section in doc['sections'] for value in [section['title'], *section['paragraphs']]]) + '\n'
            self.assertEqual(expected, doc['text'])
            self.assertEqual(expected, (ROOT / kind / f'{kind}.txt').read_text())
            self.assertEqual(sha256(expected.encode()).hexdigest(), doc['sha256'])
            self.assertNotRegex(expected, r'\[[A-Z][A-Z /]+\]')
            page = LegalPage((ROOT / kind / 'index.html').read_text())
            self.assertEqual(0, page.scripts)
            self.assertEqual(len(page.ids), len(set(page.ids)))
            self.assertTrue(set(page.anchors) <= set(page.ids))
            for section in doc['sections']:
                actual = ' '.join(page.sections[section['id']].split())
                self.assertEqual(' '.join(' '.join([section['title'], *section['paragraphs']]).split()), actual)

    def test_current_terms_are_archived_and_all_versions_are_linked(self):
        terms = json.loads((ROOT / 'legal/documents.json').read_text())['terms']
        self.assertEqual(terms['text'], (ROOT / f'terms/versions/{terms["version"]}/terms.txt').read_text())
        index = (ROOT / 'terms/versions/index.html').read_text()
        for path in (ROOT / 'terms/versions').glob('*/terms.txt'):
            self.assertIn(f'href="{path.parent.name}/"', index)
            self.assertTrue((path.parent / 'index.html').is_file())

    def test_every_main_page_exposes_terms_and_privacy(self):
        for path in ('index.html', 'terms/index.html', 'privacy/index.html', 'changelog/index.html'):
            text = (ROOT / path).read_text()
            self.assertRegex(text, r'href="(?:\.\./)?terms/"')
            self.assertRegex(text, r'href="(?:\.\./)?privacy/"')
            self.assertNotIn('<script', text.lower())
