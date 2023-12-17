from setuptools import setup, find_packages
import os
import re
import pathlib

CWD = pathlib.Path(__file__).parent.resolve()

VERSION = '1.0.0' 
with open(os.path.join(CWD, 'epub_image_helper', '__init__.py'), 'r') as f:
    re_version_pattern = re.compile(r"=[\s]*['\"]([0-9\.]+)['\"]")
    for line in f:
        line = line.strip()
        if line.find('version') >= 0:
            extractVersionInfo = re_version_pattern.search(line)
            if extractVersionInfo:
                VERSION = extractVersionInfo.group(1)

PYTHON_REQUIRES = ">=3.10"
URL = "https://github.com/changyy/epub-image-helper"
DOWNLOAD_URL = "https://pypi.org/project/epub-image-helper/"
DESCRIPTION = 'This tool allows you to easily convert specified photos and images into EPUB e-book format, making it accessible for family and friends. It can be used to create monthly or yearly photo collections for children and transform travel photos into e-books.'
LONG_DESCRIPTION = DESCRIPTION
LONG_DESCRIPTION_TYPE = 'text/plain'
try:
    with open(os.path.join(CWD, "README.md"), 'r') as f:
        data = f.read()
        if len(data) > 10:
            LONG_DESCRIPTION = data
            LONG_DESCRIPTION_TYPE = 'text/markdown'
except Exception as e:
    pass


INSTALL_REQUIRES = ['pandas']
try:
    with open(os.path.join(CWD, "requirements.txt"), 'r') as f:
        INSTALL_REQUIRES = [s.strip() for s in f.read().split("\n")]
except Exception as e:
    pass

DEPENDENCY_LINKS = []
try:
    with open(os.path.join(CWD, "deps-requirements.txt"), 'r') as f:
        DEPENDENCY_LINKS = [s.strip() for s in f.read().split("\n")]
except Exception as e:
    pass

setup(
    name="epub-image-helper", 
    version=VERSION,
    author="Yuan-Yi Chang",
    author_email="<changyy.csie@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_TYPE,
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    dependency_links=DEPENDENCY_LINKS,
    keywords=['python', 'epub', 'image', 'photo', 'album', 'pdf'],
    python_requires=PYTHON_REQUIRES,
    url=URL,
    download_url=DOWNLOAD_URL,
    entry_points={
        'console_scripts': [
            'epub-image-helper = epub_image_helper.cmd:main',
        ],
    },
    classifiers= [
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
    ]
)
