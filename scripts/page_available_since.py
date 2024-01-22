import requests
import re
import json

versions = [
    {
        "path": "/docs/",
        "name": "Latest - 5.2",
        "branch": "release-5.2"
    },
    {
        "path": "/docs/5.1/",
        "name": "5.1",
        "branch": "release-5.1"

    },
    {
        "path": "/docs/5.0/",
        "name": "5 LTS",
        "branch": "release-5"
    },
    {
        "path": "/docs/4.3/",
        "name": "4.3",
        "branch": "release-4.3"
    },
    {
        "path": "/docs/4.2/",
        "name": "4.2",
        "branch": "release-4.2"
    },
    {
        "path": "/docs/4.1/",
        "name": "4.1",
        "branch": "release-4.1"
    },
    {
        "path": "/docs/4.0/",
        "name": "4 LTS",
        "branch": "release-4"
    },
    {
        "path": "/docs/3.2/",
        "name": "3.2",
        "branch": "release-3.2"
    },
    {
        "path": "/docs/3.1/",
        "name": "3.1",
        "branch": "release-3.1"
    },
    {
        "path": "/docs/3-lts/",
        "name": "3 LTS",
        "branch": "release-3-lts"
    },

    {"path": "/docs/nightly/",
     "name": "Nightly",
     "branch": "master"
     }
]

filePath = "../tyk-docs/data/page_available_since.json"

aliases = set()


def process_and_write_to_file() -> None:
    available = get_and_process_urls()
    data_file = {"versions": versions, "pages": available}
    with open(filePath, 'w') as file:
        json.dump(data_file, file, indent=4)


def write_aliases():
    with open("aliases.txt", 'w') as file:
        ns = sorted(aliases)
        for item in ns:
            file.write(str(item) + '\n')


def get_and_process_urls():
    available_since = {}
    for version in versions:
        url = "https://tyk.io{version}pagesurl.json".format(version=version["path"])
        data = fetch_file(url)
        if 'pages' in data:
            pages = data['pages']
            for page in pages:
                url = page.get('path')
                if url:
                    if not url.startswith('/'):
                        url = '/' + url
                    if not url.endswith('/'):
                        url += '/'
                parent = page.get("parent")
                alt_url = url
                if parent is not None:
                    alt_url = parent
                    aliases.add(url)
                if url not in available_since:
                    available_since[url] = {}
                available_since[url][version["path"]] = alt_url
    for link in aliases:
        ns = available_since[link]
        similar = {}
        diff = {}
        for key, value in ns.items():
            if link == value:
                similar[key] = value
            else:
                diff[key] = value
        for dk, dv in diff.items():
            for sk, sv in similar.items():
                if sk not in available_since[dv]:
                    available_since[dv][sk] = sv
    return dict(sorted(available_since.items()))


def replace_base_url(url: str) -> str:
    version_pattern = r'https://tyk\.io/docs/[0-9]+(\.[0-9]+)?'
    replace_nightly = 'https://tyk.io/docs/nightly'
    replace_3lts = 'https://tyk.io/docs/3-lts'
    replace_latest = 'https://tyk.io/docs'
    modified_url = re.sub(version_pattern, '', url)
    modified_url = modified_url.replace(replace_nightly, '')
    modified_url = modified_url.replace(replace_3lts, '')
    modified_url = modified_url.replace(replace_latest, '')
    return modified_url


def read_file(file_name: str):
    with open(file_name, 'r') as json_file:
        data = json.load(json_file)
    return data


def fetch_file(url: str):
    print("Getting sitemap for {url}".format(url=url))
    response = requests.get(url, headers={'user-agent': 'insomnia/2023.4.0'})
    if response.status_code != 200:
        raise Exception("unable to fetch the pagesurl.json")
    response.raise_for_status()
    print("finished fetching for {url}".format(url=url))
    return response.json()


def test_modified():
    urls = [
        'https://tyk.io/docs/nightly/universal-data-graph/udg-getting-started/security/',
        'https://tyk.io/docs/5.2/universal-data-graph/udg-getting-started/security/',
        'https://tyk.io/docs/5.1/apim/',
        'https://tyk.io/docs/3.0/apim/test/is/it/docs/nightly',
        'https://tyk.io/docs/4.2/apim/itachi',
        'https://tyk.io/docs/getting-started/'
    ]
    for url in urls:
        print(replace_base_url(url))


process_and_write_to_file()