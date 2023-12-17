# epub-image-helper

[![PyPI](https://img.shields.io/pypi/v/epub-image-helper.svg)](https://pypi.org/project/epub-image-helper/)

This tool allows you to easily convert specified photos and images into EPUB e-book format, making it accessible for family and friends. It can be used to create monthly or yearly photo collections for children and transform travel photos into e-books.

## Note

```
% cat requirements.txt 
#EbookLib==0.18
git+https://github.com/changyy/ebooklib.git@release#egg=EbookLib
lxml==4.9.3
Pillow==10.1.0
PyMuPDF==1.23.7
PyMuPDFb==1.23.7
six==1.16.0
```

This tool relies on the Python library `EbookLib` to create EPUB format files. However, in the EPUB generation process of EbookLib version 0.18, the `<svg viewBox="">` syntax cannot be used properly. As a result, a fix has been proposed and contributed back to EbookLib at `https://github.com/changyy/ebooklib/tree/release` and `https://github.com/aerkalov/ebooklib/pull/297`. Once EbookLib is corrected, it will be described in a similar way to `EbookLib==0.18` after switching back.

# Usage

```
% pip install epub-image-helper
% pip install git+https://github.com/changyy/ebooklib.git@release#egg=EbookLib
% epub-image-helper
{
    "status": false,
    "input": {
        "output": "/tmp/test.epub",
        "bookConfig": "{}",
        "bookCover": "",
        "bookId": "20a3f61e-8c83-4fca-9846-afd5ffbf108a",
        "bookTitle": "Unknown",
        "bookAuthor": "Unknown",
        "epubcheck": false,
        "imageDir": [],
        "pickFirstImageToBeBookCover": false,
        "debug": false,
        "bookTableOfContent": [],
        "imageFormatConversionTable": {}
    },
    "output": {
        "path": null,
        "size": 0,
        "sizeReadable": null,
        "imageCount": 0,
        "timeCost": [
            5.9604644775390625e-06
        ]
    },
    "error": [
        "If both 'imageDir' and 'bookTableOfContent' are empty, please set at least one of them."
    ],
    "version": "1.0.0"
}

% epub-image-helper -h
usage: epub-image-helper [-h] [--output OUTPUT] [--bookConfig BOOKCONFIG] [--bookCover BOOKCOVER] [--bookTitle BOOKTITLE]
              [--bookId BOOKID] [--bookAuthor BOOKAUTHOR] [--pickFirstImageToBeBookCover] [--debug]
              [--epubcheck]
              [imageDir ...]

positional arguments:
  imageDir              the directory where the image file is located

options:
  -h, --help            show this help message and exit
  --output OUTPUT       output epub path
  --bookConfig BOOKCONFIG
                        a JSON config for EPUB builder. '@-' will read from stdin
  --bookCover BOOKCOVER
                        set a cover image for EPUB
  --bookTitle BOOKTITLE
                        set book title
  --bookId BOOKID       set book uuid info
  --bookAuthor BOOKAUTHOR
                        set book author info
  --pickFirstImageToBeBookCover
                        Select the first image as the book cover when the 'bookCover' parameter is not specified
  --debug               show bookConfig only
  --epubcheck           test output epub format via epubcheck command
```

## 1. From an image folder to an EPUB book

```
% tree 01-image-folder 
01-image-folder
├── 01.jpg
├── 02.jpg
└── 03.jpg

1 directory, 3 files

% epub-image-helper exmaple/01-image-folder 
{
    "status": true,
    "input": {
        "output": "/tmp/test.epub",
        "bookConfig": "{}",
        "bookCover": "",
        "bookId": "b717c302-b724-40aa-a9bf-dbe885b51bfb",
        "bookTitle": "Unknown",
        "bookAuthor": "Unknown",
        "epubcheck": false,
        "imageDir": [
            "exmaple/01-image-folder"
        ],
        "pickFirstImageToBeBookCover": false,
        "debug": false,
        "bookTableOfContent": [
            {
                "type": "imageDir",
                "name": "01-image-folder",
                "imageDir": "exmaple/01-image-folder"
            }
        ],
        "imageFormatConversionTable": {}
    },
    "output": {
        "path": "/tmp/test.epub",
        "size": 361025,
        "sizeReadable": "352.56 KB",
        "imageCount": 0,
        "timeCost": [
            5.221366882324219e-05,
            5.1021575927734375e-05,
            0.012903928756713867
        ]
    },
    "error": [],
    "version": "1.0.0"
}

% unzip -l /tmp/test.epub 
Archive:  /tmp/test.epub
  Length      Date    Time    Name
---------  ---------- -----   ----
       20  12-17-2023 10:32   mimetype
      251  12-17-2023 10:32   META-INF/container.xml
     1802  12-17-2023 10:32   EPUB/content.opf
       55  12-17-2023 10:32   EPUB/default.css
   128903  12-17-2023 10:32   EPUB/img-1-000002.jpg
      619  12-17-2023 10:32   EPUB/xhtml-1-000003.xhtml
    88590  12-17-2023 10:32   EPUB/img-1-000004.jpg
      619  12-17-2023 10:32   EPUB/xhtml-1-000005.xhtml
   142203  12-17-2023 10:32   EPUB/img-1-000006.jpg
      620  12-17-2023 10:32   EPUB/xhtml-1-000007.xhtml
      411  12-17-2023 10:32   EPUB/toc.ncx
      333  12-17-2023 10:32   EPUB/nav.xhtml
---------                     -------
   364426                     12 files
```

## 2. From multiple image folders to an EPUB book

```
% tree 02-multiple-image-folders 
02-multiple-image-folders
├── first
│   ├── 01.jpg
│   ├── 02.jpg
│   └── 03.jpg
└── second
    ├── 01.jpg
    ├── 02.jpg
    ├── 03.jpg
    ├── 04.jpg
    └── 05.jpg

3 directories, 8 files

% epub-image-helper exmaple/02-multiple-image-folders
{
    "status": true,
    "input": {
        "output": "/tmp/test.epub",
        "bookConfig": "{}",
        "bookCover": "",
        "bookId": "011af0b8-0340-4f5d-b22a-10dbc0a52eea",
        "bookTitle": "Unknown",
        "bookAuthor": "Unknown",
        "epubcheck": false,
        "imageDir": [
            "exmaple/02-multiple-image-folders"
        ],
        "pickFirstImageToBeBookCover": false,
        "debug": false,
        "bookTableOfContent": [
            {
                "type": "imageDir",
                "name": "02-multiple-image-folders",
                "imageDir": "exmaple/02-multiple-image-folders"
            }
        ],
        "imageFormatConversionTable": {}
    },
    "output": {
        "path": "/tmp/test.epub",
        "size": 26444959,
        "sizeReadable": "25.22 MB",
        "imageCount": 0,
        "timeCost": [
            4.696846008300781e-05,
            0.00010395050048828125,
            0.5822200775146484
        ]
    },
    "error": [],
    "version": "1.0.0"
}

% unzip -l /tmp/test.epub 
Archive:  /tmp/test.epub
  Length      Date    Time    Name
---------  ---------- -----   ----
       20  12-17-2023 10:57   mimetype
      251  12-17-2023 10:57   META-INF/container.xml
     2807  12-17-2023 10:57   EPUB/content.opf
       55  12-17-2023 10:57   EPUB/default.css
   128903  12-17-2023 10:57   EPUB/img-1-000002.jpg
      629  12-17-2023 10:57   EPUB/xhtml-1-000003.xhtml
    88590  12-17-2023 10:57   EPUB/img-1-000004.jpg
      629  12-17-2023 10:57   EPUB/xhtml-1-000005.xhtml
   142203  12-17-2023 10:57   EPUB/img-1-000006.jpg
      629  12-17-2023 10:57   EPUB/xhtml-1-000007.xhtml
 11474510  12-17-2023 10:57   EPUB/img-1-000008.jpg
      631  12-17-2023 10:57   EPUB/xhtml-1-000009.xhtml
  6709355  12-17-2023 10:57   EPUB/img-1-000010.jpg
      631  12-17-2023 10:57   EPUB/xhtml-1-000011.xhtml
  2372710  12-17-2023 10:57   EPUB/img-1-000012.jpg
      631  12-17-2023 10:57   EPUB/xhtml-1-000013.xhtml
  5484157  12-17-2023 10:57   EPUB/img-1-000014.jpg
      631  12-17-2023 10:57   EPUB/xhtml-1-000015.xhtml
   114318  12-17-2023 10:57   EPUB/img-1-000016.jpg
      630  12-17-2023 10:57   EPUB/xhtml-1-000017.xhtml
      411  12-17-2023 10:57   EPUB/toc.ncx
      333  12-17-2023 10:57   EPUB/nav.xhtml
---------                     -------
 26523664                     22 files
```

---

```
% epub-image-helper exmaple/02-multiple-image-folders/first exmaple/02-multiple-image-folders/second 
{
    "status": true,
    "input": {
        "output": "/tmp/test.epub",
        "bookConfig": "{}",
        "bookCover": "",
        "bookId": "5026a99b-257b-4c1d-bb51-d4c2fc6e3610",
        "bookTitle": "Unknown",
        "bookAuthor": "Unknown",
        "epubcheck": false,
        "imageDir": [
            "exmaple/02-multiple-image-folders/first",
            "exmaple/02-multiple-image-folders/second"
        ],
        "pickFirstImageToBeBookCover": false,
        "debug": false,
        "bookTableOfContent": [
            {
                "type": "imageDir",
                "name": "first",
                "imageDir": "exmaple/02-multiple-image-folders/first"
            },
            {
                "type": "imageDir",
                "name": "second",
                "imageDir": "exmaple/02-multiple-image-folders/second"
            }
        ],
        "imageFormatConversionTable": {}
    },
    "output": {
        "path": "/tmp/test.epub",
        "size": 26444875,
        "sizeReadable": "25.22 MB",
        "imageCount": 0,
        "timeCost": [
            5.984306335449219e-05,
            7.414817810058594e-05,
            0.5851681232452393
        ]
    },
    "error": [],
    "version": "1.0.0"
}

% unzip -l /tmp/test.epub 
Archive:  /tmp/test.epub
  Length      Date    Time    Name
---------  ---------- -----   ----
       20  12-17-2023 11:01   mimetype
      251  12-17-2023 11:01   META-INF/container.xml
     2807  12-17-2023 11:01   EPUB/content.opf
       55  12-17-2023 11:01   EPUB/default.css
   128903  12-17-2023 11:01   EPUB/img-1-000002.jpg
      609  12-17-2023 11:01   EPUB/xhtml-1-000003.xhtml
    88590  12-17-2023 11:01   EPUB/img-1-000004.jpg
      609  12-17-2023 11:01   EPUB/xhtml-1-000005.xhtml
   142203  12-17-2023 11:01   EPUB/img-1-000006.jpg
      610  12-17-2023 11:01   EPUB/xhtml-1-000007.xhtml
 11474510  12-17-2023 11:01   EPUB/img-2-000008.jpg
      612  12-17-2023 11:01   EPUB/xhtml-2-000009.xhtml
  6709355  12-17-2023 11:01   EPUB/img-2-000010.jpg
      612  12-17-2023 11:01   EPUB/xhtml-2-000011.xhtml
  2372710  12-17-2023 11:01   EPUB/img-2-000012.jpg
      612  12-17-2023 11:01   EPUB/xhtml-2-000013.xhtml
  5484157  12-17-2023 11:01   EPUB/img-2-000014.jpg
      612  12-17-2023 11:01   EPUB/xhtml-2-000015.xhtml
   114318  12-17-2023 11:01   EPUB/img-2-000016.jpg
      611  12-17-2023 11:01   EPUB/xhtml-2-000017.xhtml
      411  12-17-2023 11:01   EPUB/toc.ncx
      333  12-17-2023 11:01   EPUB/nav.xhtml
---------                     -------
 26523510                     22 files
```

## 2. Convert all images from a PDF file to an EPUB file.

```
% pdfinfo /tmp/test.pdf | grep Pages
Pages:           3

% echo '{"bookTableOfContent": [ { "type": "imagePdf", "name": "Test", "imagePdf": "/tmp/test.pdf", "workDir": "/tmp/workDir-test.pdf", "imagePdfSaveFormat": "jpg" , "imagePdfSaveQuality": 100 } ]}' | epub-image-helper --bookConfig @-
{
    "status": false,
    "input": {
        "output": "/tmp/test.epub",
        "bookConfig": "@-",
        "bookCover": "",
        "bookId": "438e9899-eafc-42ef-bc21-c0134c4f82f4",
        "bookTitle": "Unknown",
        "bookAuthor": "Unknown",
        "epubcheck": false,
        "imageDir": [],
        "pickFirstImageToBeBookCover": false,
        "debug": false,
        "bookTableOfContent": [
            {
                "type": "imagePdf",
                "name": "Test",
                "imagePdf": "/tmp/test.pdf",
                "workDir": "/tmp/workDir-test.pdf",
                "imagePdfSaveFormat": "jpg",
                "imagePdfSaveQuality": 100
            }
        ],
        "imageFormatConversionTable": {},
        "stdin": "{\"bookTableOfContent\": [ { \"type\": \"imagePdf\", \"name\": \"Test\", \"imagePdf\": \"/tmp/test.pdf\", \"workDir\": \"/tmp/workDir-test.pdf\", \"imagePdfSaveFormat\": \"jpg\" , \"imagePdfSaveQuality\": 100 } ]}\n"
    },
    "output": {
        "path": null,
        "size": 0,
        "sizeReadable": null,
        "imageCount": 0,
        "timeCost": [
            2.9087066650390625e-05,
            3.0279159545898438e-05
        ]
    },
    "error": [
        {
            "status": false,
            "error": [
                "type=\"imagePdf\" error, \"workDir\" not exists: index=0, item={'type': 'imagePdf', 'name': 'Test', 'imagePdf': '/tmp/test.pdf', 'workDir': '/tmp/workDir-test.pdf', 'imagePdfSaveFormat': 'jpg', 'imagePdfSaveQuality': 100}"
            ],
            "input": [
                {
                    "type": "imagePdf",
                    "name": "Test",
                    "imagePdf": "/tmp/test.pdf",
                    "workDir": "/tmp/workDir-test.pdf",
                    "imagePdfSaveFormat": "jpg",
                    "imagePdfSaveQuality": 100
                }
            ],
            "output": [],
            "totalImage": 0,
            "timeCost": []
        }
    ],
    "version": "1.0.0"
}

% mkdir /tmp/workDir-test.pdf

% echo '{"bookTableOfContent": [ { "type": "imagePdf", "name": "Test", "imagePdf": "/tmp/test.pdf", "workDir": "/tmp/workDir-test.pdf", "imagePdfSaveFormat": "jpg" , "imagePdfSaveQuality": 100 } ]}' | epub-image-helper --bookConfig @-
{
    "status": true,
    "input": {
        "output": "/tmp/test.epub",
        "bookConfig": "@-",
        "bookCover": "",
        "bookId": "1e788bee-4f66-49f5-bce3-c412a7a4a348",
        "bookTitle": "Unknown",
        "bookAuthor": "Unknown",
        "epubcheck": false,
        "imageDir": [],
        "pickFirstImageToBeBookCover": false,
        "debug": false,
        "bookTableOfContent": [
            {
                "type": "imagePdf",
                "name": "Test",
                "imagePdf": "/tmp/test.pdf",
                "workDir": "/tmp/workDir-test.pdf",
                "imagePdfSaveFormat": "jpg",
                "imagePdfSaveQuality": 100
            }
        ],
        "imageFormatConversionTable": {},
        "stdin": "{\"bookTableOfContent\": [ { \"type\": \"imagePdf\", \"name\": \"Test\", \"imagePdf\": \"/tmp/test.pdf\", \"workDir\": \"/tmp/workDir-test.pdf\", \"imagePdfSaveFormat\": \"jpg\" , \"imagePdfSaveQuality\": 100 } ]}\n"
    },
    "output": {
        "path": "/tmp/test.epub",
        "size": 361006,
        "sizeReadable": "352.54 KB",
        "imageCount": 0,
        "timeCost": [
            3.0994415283203125e-05,
            0.035225868225097656,
            0.013682126998901367
        ]
    },
    "error": [],
    "version": "1.0.0"
}

% unzip -l /tmp/test.epub 
Archive:  /tmp/test.epub
  Length      Date    Time    Name
---------  ---------- -----   ----
       20  12-17-2023 13:37   mimetype
      251  12-17-2023 13:37   META-INF/container.xml
     1802  12-17-2023 13:37   EPUB/content.opf
       55  12-17-2023 13:37   EPUB/default.css
   128903  12-17-2023 13:37   EPUB/img-1-000002.jpg
      608  12-17-2023 13:37   EPUB/xhtml-1-000003.xhtml
    88590  12-17-2023 13:37   EPUB/img-1-000004.jpg
      608  12-17-2023 13:37   EPUB/xhtml-1-000005.xhtml
   142203  12-17-2023 13:37   EPUB/img-1-000006.jpg
      609  12-17-2023 13:37   EPUB/xhtml-1-000007.xhtml
      411  12-17-2023 13:37   EPUB/toc.ncx
      333  12-17-2023 13:37   EPUB/nav.xhtml
---------                     -------
   364393                     12 files
```
