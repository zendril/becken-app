import copy
from html.parser import HTMLParser
import json
import unittest
import build_changelog as builder

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=[]; self.anchors=[]; self.scripts=0
    def handle_starttag(self, tag, attributes):
        attrs=dict(attributes)
        if 'id' in attrs:self.ids.append(attrs['id'])
        if tag == 'a' and attrs.get('href','').startswith('#'):self.anchors.append(attrs['href'][1:])
        if tag == 'script':self.scripts+=1

class ChangelogTest(unittest.TestCase):
    def setUp(self):
        self.data=json.loads((builder.ROOT/'changelog/releases.json').read_text())

    def test_every_jump_link_resolves_and_ids_are_unique(self):
        parser=Links();parser.feed(builder.render(self.data))
        self.assertEqual(len(parser.ids),len(set(parser.ids)))
        self.assertTrue(set(parser.anchors) <= set(parser.ids))
        self.assertEqual(0,parser.scripts)
        self.assertEqual(len(self.data['releases']),sum(id.startswith('v') for id in parser.ids))

    def test_prose_is_escaped_as_text(self):
        self.data['releases'][0]['title']='<script>alert("bad")</script>'
        self.data['releases'][0]['added']=['<img src=x onerror=alert(1)> & test']
        html=builder.render(self.data)
        self.assertNotIn('<script>',html)
        self.assertNotIn('<img src=x',html)
        self.assertIn('&lt;img src=x',html)

    def test_development_does_not_get_a_release_date(self):
        self.data['releases'][0]['channel']='development'
        self.data['releases'][0]['releasedOn']='2026-10-20'
        with self.assertRaises(ValueError):builder.render(self.data)

    def test_unknown_formats_and_fields_are_rejected(self):
        for key,value in [('version',2),('privateNote','secret')]:
            data=copy.deepcopy(self.data);data[key]=value
            with self.assertRaises(ValueError):builder.render(data)

if __name__ == '__main__':unittest.main()
