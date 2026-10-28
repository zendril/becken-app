#!/usr/bin/env python3
"""Render and check the same static header navigation on every website page."""
import argparse
from html import escape
from pathlib import Path, PurePosixPath
import re

ROOT = Path(__file__).resolve().parents[1]
LINKS = (
    ('#screenshots', 'The app'),
    ('guides/ai-workouts/', 'AI workout guide'),
    ('changelog/', 'Changelog'),
    ('terms/', 'Terms'),
    ('privacy/', 'Privacy'),
)
MAIN_NAV = re.compile(r'<nav aria-label="Main navigation">.*?</nav>', re.DOTALL)


def render_navigation(directory):
    directory = PurePosixPath(directory)
    prefix = '../' * len(directory.parts)
    links = []
    for target, label in LINKS:
        current = ' aria-current="page"' if target.rstrip('/') == directory.as_posix() else ''
        links.append(f'<a href="{prefix}{target}"{current}>{escape(label)}</a>')
    return '<nav aria-label="Main navigation">' + ''.join(links) + '</nav>'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('--write', action='store_true')
    action.add_argument('--check', action='store_true')
    args = parser.parse_args()
    pages = sorted(ROOT.rglob('*.html'))
    for path in pages:
        text = path.read_text()
        relative = path.relative_to(ROOT)
        if len(MAIN_NAV.findall(text)) != 1:
            raise ValueError(f'Expected one main navigation in {relative}')
        expected = MAIN_NAV.sub(lambda _: render_navigation(relative.parent.as_posix()), text)
        if args.write:
            path.write_text(expected)
        elif text != expected:
            raise ValueError(f'Inconsistent header navigation in {relative}; run scripts/site_navigation.py --write')
    print(f'Header navigation {"written" if args.write else "checked"}: {len(pages)} pages')


if __name__ == '__main__':
    main()
