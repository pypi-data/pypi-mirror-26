"""
Contains the fixtures used by the dploy tests
"""

import pytest
import utils


@pytest.fixture()
def source_a(tmpdir):
    """
    a source directory to stow and unstow
    """
    name = str(tmpdir.join('source_a'))
    tree = [
        {
            name: [
                {
                    'aaa': [
                        'aaa',
                        'bbb',
                        {
                            'ccc': [
                                'aaa',
                                'bbb',
                            ],
                        },
                    ],
                },
            ],
        },
    ]
    utils.create_tree(tree)
    return name


@pytest.fixture()
def source_b(tmpdir):
    """
    a source directory to stow and unstow
    """
    name = str(tmpdir.join('source_b'))
    tree = [
        {
            name: [
                {
                    'aaa': [
                        'ddd',
                        'eee',
                        {
                            'fff': [
                                'aaa',
                                'bbb',
                            ],
                        },
                    ],
                },
            ],
        },
    ]
    utils.create_tree(tree)
    return name


@pytest.fixture()
def source_d(tmpdir):
    """
    a source directory to stow and unstow
    """
    name = str(tmpdir.join('source_d'))
    tree = [
        {
            name: [
                {
                    'aaa': [
                        'ggg',
                        'hhh',
                        {
                            'iii': [
                                'aaa',
                                'bbb',
                            ],
                        },
                    ],
                },
            ],
        },
    ]
    utils.create_tree(tree)
    return name


@pytest.fixture()
def source_c(tmpdir):
    """
    a source directory to stow and unstow identical to source_a
    """
    name = str(tmpdir.join('source_c'))
    tree = [
        {
            name: [
                {
                    'aaa': [
                        'aaa',
                        'bbb',
                        {
                            'ccc': [
                                'aaa',
                                'bbb',
                            ],
                        },
                    ],
                },
            ],
        },
    ]
    utils.create_tree(tree)
    return name


@pytest.fixture()
def source_only_files(tmpdir):
    """
    a source directory to stow and unstow that only contains files
    """
    name = str(tmpdir.join('source_only_files'))
    tree = [{
        name: [
            'aaa',
        ]
    }]
    utils.create_tree(tree)
    return name


@pytest.fixture()
def dest(tmpdir):
    """
    a destination directory to stow into or unstow from
    """
    name = str(tmpdir.join('dest'))
    utils.create_directory(name)
    return name


@pytest.fixture()
def file_a(tmpdir):
    """
    creates a file
    """
    name = str(tmpdir.join('file_a'))
    utils.create_file(name)
    return name


@pytest.fixture()
def file_b(tmpdir):
    """
    creates a file
    """
    name = str(tmpdir.join('file_b'))
    utils.create_file(name)
    return name


@pytest.fixture()
def file_dploystowignore(tmpdir):
    """
    creates an empty ignore file file
    """
    name = str(tmpdir.join('.dploystowignore'))
    utils.create_file(name)
    return name
