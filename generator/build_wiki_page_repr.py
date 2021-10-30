"""Generation of specific remote dokuwiki pages,
to specified website pages in markdown, for pelican.

"""

import os
import re
import datetime
import subprocess
import configparser
try:
    from dokuwikixmlrpc import DokuWikiClient, DokuWikiXMLRPCError
except ImportError:
    print('Python package dokuwikixmlrpc not installed.')
    print('You may want to run something like `pip3 install dokuwikixmlrpc --user -U`')
    exit(1)

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__)).rstrip('/') + '/'
INI_FILE = SCRIPT_PATH + 'wiki-access.ini'
INI_FILE_TEMPLATE = SCRIPT_PATH + 'wiki-template.ini'
CONVERT_USING_PANDOC = False

def read_ini_file():
    config_parser = configparser.ConfigParser()
    config_parser.read(INI_FILE)
    pages = {}
    for section in config_parser.sections():
        if section == 'META':  continue
        cp = config_parser[section]
        pages[section] = cp['title'], cp['slug'], cp['wikipage'], cp.get('summary', ''), cp.get('tags', '')
    cp = config_parser['META']
    return cp['wiki_url'], cp['wiki_username'], cp['wiki_password'], cp['target_dir'], pages

try:
    WIKI_URL, WIKI_USERNAME, WIKI_PASSWORD, TARGET_DIR, WIKI_PAGES = read_ini_file()
except Exception as err:
    print(f"Invalid config file {INI_FILE}: {repr(err)}")
    print("It must look like the provided template ({INI_FILE_TEMPLATE}):\n")
    with open(INI_FILE_TEMPLATE) as fd:
        print(''.join('\t'+line.strip()+'\n' for line in fd.readlines()))
    print("\nAbort.")
    exit(1)


def read_dokuwiki_page_as_markdown(client, page: str) -> str:
    dk_data = client.page(page)
    if CONVERT_USING_PANDOC:
        with open('.temp.txt', 'w') as fd:
            fd.write(dk_data)
        proc = subprocess.Popen(['pandoc', '.temp.txt', '--from', 'dokuwiki', '--to', 'markdown', '-o', '.temp.mkd'])
        proc.communicate()
        with open('.temp.mkd') as fd:
            return fd.read()
    else:
        return convert_to_markdown_by_regexes(dk_data)


def convert_to_markdown_by_regexes(dk_data: str):
    trans = {
        # titles
        r' *=====([^=]*)=* *': r'#\1',
        r' *====([^=]*)=* *': r'##\1',
        r' *===([^=]*)=* *': r'###\1',
        r' *==([^=]*)=* *': r'####\1',
        r' *=([^=]*)=* *': r'#####\1',
        # lists
        r'(\n *[^\*\- ].*\n)(   *[*-])': r'\1\n\2',  # add a blank line before lists
        r'^( *)  - ': r'(\1)1. ',
        r'^( *)  * ': r'\1\* ',
        # styles
        r'\*\*(.+)\*\*': r'\*\*\1\*\*',
        r'\/\/(.+)\/\/': r'\*\1\*',
        r'\_\_(.+)\_\_': r'<u>\1</u>',
        r'\'\'(.+)\'\'': r'`\1`',
        r'<del>(.+)</del>': r'~~\1~~',
        # images and links
        r'\{\{([^|]+)\}\}': r'[image](\1)',
        r'\{\{(.+)|(.+)\}\}': r'[\1](\2)',
        r'\[\[(.+)|(.+)\]\]': r'[\1](\2)',
        r'\[\[(.+)\]\]': r'[\1](\1)',
    }
    for pattern, repl in trans.items():
        # print(repr(pattern), repr(repl))
        dk_data = re.sub(pattern, repl, dk_data)
    return dk_data


def whole_markdown_page(client, page_title: str, page_slug: str, wiki_page: str, summary: str, tags: str) -> [str]:
    """Yield paragraphs of markdown to write in output file"""
    metadatas = {
        'Title': page_title,
        'Date': datetime.datetime.now().strftime('%Y-%m-%d'),
        'Tags': tags,
        'Summary': summary,
        'Slug': page_slug,
        'Status': 'published',
    }
    yield '\n'.join(f'{k}: {v}' for k, v in metadatas.items())
    yield read_dokuwiki_page_as_markdown(client, wiki_page)


if __name__ == "__main__":
    client = DokuWikiClient(WIKI_URL, WIKI_USERNAME, WIKI_PASSWORD)
    for args in WIKI_PAGES.values():
        slug = args[1]
        with open(os.path.join(TARGET_DIR, slug + '.mkd'), 'w') as fd:
            fd.write('\n\n'.join(whole_markdown_page(client, *args)))
