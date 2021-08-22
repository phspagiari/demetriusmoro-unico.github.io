"""Mkdocs pre-build script to merge multiple repos into one doc structure."""

import fileinput
import logging
import os
import shutil

from git import Repo
import yaml


BASE_PATH = 'mkdocs'
TEMP_PATH = f'{BASE_PATH}/docs/temp'
ENCODING = 'utf-8'
MKDOCS_YML = f'{BASE_PATH}/mkdocs.yml'
REPO_NOT_AVAILLABLE_MD = 'external.md'


fetch_dependencies = (os.environ.get('FETCH_DEPENDENCIES', '0') == "1")
cloned_repos = []


def run():
    """Script entrypoint"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s'
    )

    logging.info('*** BEGIN')

    logging.info('fecth_dependencies=%s', fetch_dependencies)
    merge_confs()
    update_nav_file()
    del_temp_files()

    logging.info('*** END')


def merge_confs():
    """Merges conf and nav files into one be used by the mkdocs builder."""
    logging.info('Merging confs')

    with open(f'{BASE_PATH}/conf.yml', 'r', encoding=ENCODING) as yml_file:
        conf_yml = yml_file.read()

    with open(f'{BASE_PATH}/nav.yml', 'r', encoding=ENCODING) as yml_file:
        nav_yml = yml_file.read()

    with open(MKDOCS_YML, 'w', encoding=ENCODING) as yml_file:
        yml_file.write(f'{conf_yml}\n{nav_yml}')
        yml_file.close()


def update_nav_file():
    """Replaces placeholders on nav file."""
    logging.info('Updating nav file')

    with open(MKDOCS_YML, 'r', encoding=ENCODING) as yml_file:
        doc_tree = yaml.load(yml_file, Loader=yaml.FullLoader)

    with open(MKDOCS_YML, 'w', encoding=ENCODING) as yml_file:
        doc_tree['nav'] = update_nav_tree(doc_tree['nav'])
        yaml.dump(doc_tree, yml_file, encoding=ENCODING)


def update_nav_tree(nav_item):
    """Replaces repo placeholders on nav item."""

    if isinstance(nav_item, list):
        for i, _ in enumerate(nav_item):
            nav_item[i] = update_nav_tree(nav_item[i])
        return nav_item

    if isinstance(nav_item, dict):
        for k in nav_item.keys():
            nav_item[k] = update_nav_tree(nav_item[k])
        return nav_item

    if isinstance(nav_item, str) and nav_item.lower().endswith('.git'):
        return (
            expand_repo(nav_item)
            if fetch_dependencies
            else REPO_NOT_AVAILLABLE_MD
        )

    return nav_item


def expand_repo(repo_url):
    """Expands a repo url into its mkdocs nav structure."""

    logging.info('Clonning %s', repo_url)
    repo_name = repo_url.lower().split('/')[-1:][0][0:-4]
    repo_path = f'{TEMP_PATH}/{repo_name}'
    nav_file = f'{repo_path}/mkdocs/nav.yml'
    doc_folder_repo = f'{repo_path}/mkdocs/doc'
    doc_folder_build = f'{BASE_PATH}/docs/doc/{repo_name}'
    clone_repo(repo_url, repo_path)

    logging.info('Expanding %s', repo_path)
    with fileinput.FileInput(nav_file, inplace=True, backup='.bak') as yml_file:
        for line in yml_file:
            new_line = (
                line
                if f' doc/{repo_name}/' in line
                else line.replace(' doc/', f' doc/{repo_name}/')
            )

            print(new_line, end='')

    with open(nav_file, 'r', encoding='utf8') as yml_file:
        nav_yml = yaml.load(yml_file, Loader=yaml.FullLoader)['nav']

    logging.info('Copying %s', doc_folder_repo)
    if os.path.exists(doc_folder_build):
        shutil.rmtree(doc_folder_build)

    shutil.copytree(
        os.path.abspath(doc_folder_repo),
        os.path.abspath(doc_folder_build),
    )

    return nav_yml


def clone_repo(repo_url, repo_path):
    """Clones a repo from github on the local folder."""

    if repo_url in cloned_repos:
        raise Exception('Duplicated external-repo references, build aborted.')

    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)

    Repo.clone_from(
        url=repo_url,
        to_path=repo_path,
        env=dict({'GIT_TERMINAL_PROMPT': '0'}),
    )

    cloned_repos.append(repo_url)


def del_temp_files():
    """Removes unused files to avoid warnings because of build files."""
    logging.info('Cleanning temp files')

    if not fetch_dependencies:
        return

    shutil.rmtree(TEMP_PATH)
    os.remove(f'{BASE_PATH}/docs/{REPO_NOT_AVAILLABLE_MD}')


if __name__ == '__main__':
    run()
