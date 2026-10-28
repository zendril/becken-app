import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import build_workout_schemas as site


class WorkoutSiteTest(unittest.TestCase):
    def test_all_published_examples_validate_and_pages_link_raw_json(self):
        pages=site.outputs()
        self.assertIn(site.ROOT/'guides/ai-workouts/index.html',pages)
        release=pages[site.ROOT/'schemas/workout/release/index.html']
        self.assertIn('href="schema.json"',release)
        self.assertIn('href="example.json"',release)
        self.assertIn('Routines → Import',release)
        self.assertNotIn('<script',release)

    def test_guide_covers_user_preferences_download_and_import_repair(self):
        guide=site.outputs()[site.ROOT/'guides/ai-workouts/index.html']
        for phrase in ['Gemini','ChatGPT','Claude','goals','avoid','intensity','days per week','UTF-8','Import routine','error message','schema.json','example.json']:
            self.assertIn(phrase,guide)

    def test_corrupt_or_stale_contract_stops_generation(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);shutil.copytree(site.ROOT/'schemas',root/'schemas')
            target=root/'schemas/workout/release/example.json'
            target.write_text(target.read_text()+' ')
            with patch.object(site,'ROOT',root),self.assertRaisesRegex(ValueError,'checksum'):site.outputs()

    def test_private_or_unknown_metadata_is_not_published(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);shutil.copytree(site.ROOT/'schemas',root/'schemas')
            target=root/'schemas/workout/release/manifest.json';data=json.loads(target.read_text());data['internalSource']='private'
            target.write_text(json.dumps(data))
            with patch.object(site,'ROOT',root),self.assertRaisesRegex(ValueError,'metadata'):site.outputs()

    def test_schema_and_example_text_are_html_escaped(self):
        original=site.read_contract
        def read(folder, release=False):
            meta,schema,example=original(folder,release)
            example['routine']['name']='<script>unsafe</script>'
            return meta,schema,example
        with patch.object(site,'read_contract',side_effect=read):
            page=site.render_contract(site.ROOT/'schemas/workout/release',True)
        self.assertNotIn('<script>',page)
        self.assertIn('&lt;script&gt;',page)


if __name__ == '__main__':unittest.main()
