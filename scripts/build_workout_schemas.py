#!/usr/bin/env python3
"""Validate published import contracts and render their static documentation."""
import argparse
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import re
from jsonschema import Draft202012Validator
from site_navigation import render_navigation

ROOT = Path(__file__).resolve().parents[1]

AI_PROMPT = '''Help me create a workout routine that I can import into Becken.

My goals: [strength, muscle growth, general fitness, or another goal]
My training experience: [beginner, returning, experienced]
Available equipment: [list what I can use]
Movements to avoid or modify: [list restrictions and preferred alternatives]
Schedule: [days per week and minutes per session]
Desired intensity: [easy, moderate, challenging; include recovery preferences]
Weight units: [lb or kg]
Exercise preferences: [include carries, timed holds, or other preferences]

Use the current Becken import schema:
https://becken.app/schemas/workout/release/schema.json
Use this valid example as a format reference:
https://becken.app/schemas/workout/release/example.json
Compatibility information:
https://becken.app/schemas/workout/release/

If you cannot read these URLs, ask me to attach the schema and example.
Ask any necessary clarifying questions before suggesting a routine. Explain
how the proposed routine fits my goals, schedule and desired intensity.
Once we agree, create a UTF-8 .json file that follows that schema exactly.
Use its exact format and version. Include only fields supported by the schema.
Keep exercise IDs unique and references valid. Importable routines are not backups.
Use starting values only as optional suggestions. Distinguish combined dumbbell
weight from weight per hand. Use exactly one measurement for each exercise entry,
and only use time or distance when supported by the linked schema.
For a one-handed carry, describe one side per set and include sets for both sides.
Validate the JSON against the schema if you have a validation tool available;
otherwise say that you have not run a validator. Do not claim validation you did not run.
Return the final file, or its JSON content alone without Markdown code fences.
'''


def require(condition, message):
    if not condition: raise ValueError(message)


def read_contract(folder, release=False):
    meta = json.loads((folder / 'manifest.json').read_text())
    fields = {'format', 'version', 'schemaVersion', 'minimumAppVersion', 'schemaSha256', 'exampleSha256'}
    require(set(meta) == fields | ({'appVersion', 'versionCode'} if release else set()), 'Unexpected metadata fields')
    require(meta['format'] == 'becken.workout-schema' and type(meta['version']) is int and meta['version'] == 1, 'Unsupported metadata')
    require(type(meta['schemaVersion']) is int and meta['schemaVersion'] > 0, 'Invalid schema version')
    require(re.fullmatch(r'\d+\.\d+\.\d+', meta['minimumAppVersion']), 'Invalid minimum app version')
    if release:
        require(re.fullmatch(r'\d+\.\d+\.\d+', meta['appVersion']), 'Invalid app version')
        major, minor, patch = map(int, meta['appVersion'].split('.'))
        require(type(meta['versionCode']) is int and meta['versionCode'] == major * 1000000 + minor * 1000 + patch, 'App version/code mismatch')
        require(tuple(map(int, meta['minimumAppVersion'].split('.'))) <= (major, minor, patch), 'Unsupported release contract')
    documents = {}
    for name in ('schema', 'example'):
        content = (folder / f'{name}.json').read_bytes()
        require(len(content) <= 2 * 1024 * 1024, 'Contract file too large')
        require(sha256(content).hexdigest() == meta[f'{name}Sha256'], 'Stale contract checksum')
        documents[name] = json.loads(content)
    schema, example = documents['schema'], documents['example']
    def refs(value):
        if isinstance(value, dict):
            require('$ref' not in value or value['$ref'].startswith('#/'), 'External schema reference')
            for child in value.values(): refs(child)
        elif isinstance(value, list):
            for child in value: refs(child)
    refs(schema)
    require(schema['properties']['format']['const'] == 'liftlog.routine' and schema['properties']['version']['const'] == meta['schemaVersion'], 'Schema metadata mismatch')
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(example)
    definitions = [e['id'] for e in example['exercises']]
    require(len(set(definitions)) == len(definitions), 'Duplicate exercise IDs')
    for day in example['routine']['days']:
        ids = [e['exerciseId'] for e in day['exercises']]
        require(len(set(ids)) == len(ids) and set(ids) <= set(definitions), 'Invalid exercise references')
        pairs = [e['pairId'] for e in day['exercises'] if e.get('pairId') is not None]
        require(all(pairs.count(p) == 2 for p in pairs), 'Invalid exercise pair')
    return meta, schema, example


def shell(title, path, content):
    prefix = '../' * len(Path(path).parts)
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#081722"><title>{escape(title)} — Becken</title>
<meta name="description" content="Create and import a Becken workout routine using the documented JSON schema and a downloadable example.">
<link rel="canonical" href="https://becken.app/{path}/"><link rel="icon" href="{prefix}assets/logo.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}styles.css"></head>
<body><!-- Generated by scripts/build_workout_schemas.py. -->
<a class="skip-link" href="#main">Skip to content</a><header class="site-header wrap">
<a class="brand" href="{prefix}" aria-label="Becken home"><img src="{prefix}assets/logo.svg" width="42" height="42" alt=""><span>Becken</span></a>
{render_navigation(path)}</header>
<main id="main" class="policy wrap workout-guide"><h1>{escape(title)}</h1>{content}</main>
<footer class="site-footer wrap"><span class="footer-brand">Becken <span>Make the next rep count.</span></span><a href="{prefix}">Home</a><a href="{prefix}schemas/workout/">Workout schemas</a><a href="{prefix}terms/">Terms</a><a href="{prefix}privacy/">Privacy</a></footer></body></html>
'''


def render_contract(folder, release=False):
    meta, schema, example = read_contract(folder, release)
    title = 'Workout import schema · ' + ('release' if release else f'v{meta["schemaVersion"]}')
    compatible = (f'<p>Release follows the latest shipped Play build, currently <strong>{escape(meta["appVersion"])}</strong>. Becken is in private Internal testing; this does not announce public availability.</p>' if release else '')
    fields = schema['$defs']['entry']['properties']
    rows = ''.join(f'<tr><th scope="row"><code>{escape(name)}</code></th><td>{escape(json.dumps(description, ensure_ascii=False))}</td></tr>' for name, description in fields.items() if name != 'id')
    content = f'''{compatible}<p>This file creates a reusable routine using <code>liftlog.routine</code>, schema <strong>{meta['schemaVersion']}</strong>. It imports into Becken <strong>{escape(meta['minimumAppVersion'])}</strong> and later versions supporting this schema.</p>
<p><a href="schema.json">Read or download the JSON Schema</a> · <a href="example.json" download="becken-workout.json">Download example workout</a> · <a href="../../../guides/ai-workouts/">Create a workout with AI</a></p>
<p>Import with <strong>Routines → Import</strong>, then review the preview. Import creates a new routine; it does not replace an existing routine or restore a backup.</p>
<h2>File structure</h2><p>Supply exercise definitions in <code>exercises</code>, and a named <code>routine</code> with its weight unit and ordered days. Each day's entries reference an exercise ID. Use the exact format, version and fields in the linked schema.</p>
<h2>Exercise entries</h2><div class="table-scroll"><table><thead><tr><th>Field</th><th>Schema rule</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2>Units and import rules</h2><p>Starting weights use the routine's lb or kg unit. Dumbbells use <code>perHand: true</code> for weight in each hand or <code>false</code> for combined weight. Bodyweight entries record added weight, with 0 for unweighted. Starting values are suggestions and never count as completed work.</p>
<p>Files must be UTF-8 JSON under 2 MiB, with unique IDs, valid exercise references, no repeated exercise within a day, and exactly two entries for each non-null pair ID. The schema describes structure; Becken additionally checks references and pairs. Unknown fields and unsupported versions are rejected.</p>
<h2>Example</h2><p>These quantities demonstrate the file format; adapt the routine to your own goals and experience.</p><pre><code>{escape(json.dumps(example, indent=2, ensure_ascii=False))}</code></pre>
<p><a href="../">All published schema versions</a></p>'''
    return shell(title, folder.relative_to(ROOT).as_posix(), content)


def outputs():
    base = ROOT / 'schemas/workout'
    folders = sorted((p for p in base.iterdir() if p.is_dir() and re.fullmatch(r'v[1-9]\d*', p.name)), key=lambda p: int(p.name[1:]))
    release_meta, _, _ = read_contract(base / 'release', True)
    archived = base / f'v{release_meta["schemaVersion"]}'
    for name in ('schema.json', 'example.json'):
        require((base / 'release' / name).read_bytes() == (archived / name).read_bytes(), 'Release and archive differ')
    archive_meta, _, _ = read_contract(archived)
    require(archive_meta == {k: v for k, v in release_meta.items() if k not in ('appVersion', 'versionCode')}, 'Archive metadata differs')
    result = {folder / 'index.html': render_contract(folder) for folder in folders}
    result[base / 'release/index.html'] = render_contract(base / 'release', True)
    links = ''.join(f'<li><a href="{p.name}/">Schema {p.name}</a></li>' for p in reversed(folders))
    result[base / 'index.html'] = shell('Workout import schemas', 'schemas/workout', f'<p><a href="release/">Current release schema and example</a> · <a href="../../guides/ai-workouts/">AI workout guide</a></p><p>Release follows the shipped app. App versions and schema versions are independent. Older schema URLs remain available.</p><h2>Published versions</h2><ul>{links}</ul>')
    result[ROOT / 'guides/ai-workouts/index.html'] = shell('Create a workout with AI', 'guides/ai-workouts', f'''
<p class="intro">Describe the training you want. Turn it into a routine you can import into Becken.</p>
<p>You can use Gemini, ChatGPT or Claude to help write the file. The same prompt works with any assistant that can produce JSON. Becken does not connect to an AI account, and this page does not collect your answers.</p>
<h2>1. Describe what works for you</h2>
<p>Start with your goals and experience. Tell the AI what equipment you have, which movements to avoid or modify, how often you want to train, how long each session should be, and how hard you want to work. Include recovery days and exercise preferences. These details shape the routine; they are not extra fields to add to the import file.</p>
<h2>2. Give the AI the format</h2>
<p>Use the <a href="../../schemas/workout/release/">current release schema and example</a>. Check its compatible app version against the version in Becken Settings. Update Becken or choose an <a href="../../schemas/workout/">older published schema</a> if needed.</p>
<p>Copy this prompt into your preferred assistant and replace the bracketed details. If it cannot open the links, download and attach <a href="../../schemas/workout/release/schema.json" download="becken-schema.json">the schema</a> and <a href="../../schemas/workout/release/example.json" download="becken-example.json">the example</a>. Keep the requested file within the schema's supported features.</p>
<pre class="ai-prompt"><code>{escape(AI_PROMPT)}</code></pre>
<h2>3. Review and save the file</h2>
<p>Review the proposed exercises, schedule, intensity and starting suggestions. AI output can contain mistakes; adjust anything that does not fit your goals or restrictions. Then ask for the final file.</p>
<p>Download it as <code>my-workout.json</code>. If the assistant only provides text, copy the JSON into a plain-text editor and save it as UTF-8 with the <code>.json</code> extension. Leave out chat explanations and Markdown fences.</p>
<h2>4. Import into Becken</h2>
<ol><li>Open <strong>Routines → Import</strong>.</li><li>Select your JSON file.</li><li>Review the routine name, units, days and exercises in the preview.</li><li>Choose <strong>Import routine</strong>, then open the routine to review its starting suggestions.</li></ol>
<p>Import adds a new routine. Starting suggestions are not completed workout results. A full backup uses a different format and belongs in Settings, not routine import.</p>
<h2>If import reports an error</h2>
<p>Copy the error message back to the AI together with the same schema and ask it to repair the file. Check that the file contains JSON only, uses a supported schema version, and is under 2 MiB. Unsupported fields, missing exercise references, duplicate exercises within a day and incomplete pairs can prevent import.</p>
<p><a href="../../schemas/workout/release/example.json" download="becken-example.json">Try the downloadable example</a> to check the import steps. Its quantities illustrate the format and are not a personalized training prescription.</p>
''')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write', action='store_true'); group.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for path, content in outputs().items():
        if args.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        else: require(path.exists() and path.read_text() == content, f'Stale schema page: {path}')
    print('Workout schemas, examples and generated pages are current.')


if __name__ == '__main__':
    main()
