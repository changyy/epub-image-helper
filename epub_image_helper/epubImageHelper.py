# -*- encoding: utf-8 -*-

import os
from ebooklib import epub
import fitz
from PIL import Image
from io import BytesIO
import uuid
import time

from epub_image_helper import common

class EPUBImageHelper:
    def __init__(self, outputEPUBPath: str = '/tmp/test.epub', imageBookId: str = str(uuid.uuid4()), imageBookTitle: str = 'Unknown', imageBookLanguage: str = 'en', imageBookAuthor: list[str] = ['Test'], tableOfContent: list[dict[str, list[str]]] = [], pickFirstImageToBeBookCover: bool = False, imageBookPageProgressionDirection: str = 'rtl', imageBookOpfMeta: list[dict] = []):
        self.outputEPUBPath = outputEPUBPath
        self.bookId = imageBookId
        self.bookTitle = imageBookTitle
        self.bookLanguage = imageBookLanguage
        self.bookAuthor = imageBookAuthor
        self.hasBookCover = False
        self.pickFirstImageToBeBookCover = pickFirstImageToBeBookCover
        self.bookCoverBytes = None
        self.bookCoverFilename = 'defaultCover.jpg'
        self.bookPageProgressionDirection = imageBookPageProgressionDirection
        self.bookOpfMeta = imageBookOpfMeta
        self.tableOfContent = tableOfContent
        self.objectId = 0
        self.imageFormatConversionTable = {}
        self.cssMainUsageName = 'main.css'
        self.cssImageUsageName = 'image.css'
        self.jsMainUsageName = 'main.js'
        self.jsImageUsageName = 'image.js'

        self.xhtmlResource = {
            'javascript': {
                self.jsMainUsageName: '''
                ''',
                self.jsImageUsageName: '''
                '''
            },
            'style': {
                self.cssMainUsageName: '''
@charset "UTF-8";
html, body { margin: 0; padding: 0; }
                ''',
                self.cssImageUsageName: '''
   html, body {
     margin: 0;
     padding: 0;
     width: 100%;
     height: 100%;
     display: flex;
     align-items: center;
     justify-content: center;
   }

   svg {
     width: 100%;
     height: 100%;
   }

   image {
     width: 100%;
     height: 100%;
     object-fit: contain;
   }
                '''
            }
        }
        self.xhtmlTemplate = {
            "image": '''
<svg 
  xmlns="http://www.w3.org/2000/svg" version="1.1"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  width="100%" height="100%" viewBox="0 0 {imageWidth} {imageHeight}">
  <image xlink:href="{imagePath}" width="{imageWidth}" height="{imageHeight}" />
</svg>
''',
        }

    def setPageProgressionDirection(self, pageProgressionDirection):
        if pageProgressionDirection in ['rtl', 'rtl', 'default']:
            self.bookPageProgressionDirection = pageProgressionDirection

    def setTableOfContent(self, inputTOC: list[dict]) -> dict:
        checker = self.veirfyTableOfContent(inputTOC)
        if checker['status']:
            self.tableOfContent = checker['output']
        return checker

    def veirfyTableOfContent(self, inputTOC: list[dict] = []) -> dict:
        output = {"status": False, "error": [], 'input': inputTOC, 'output': [], 'totalImage': 0, 'timeCost': []}
        if inputTOC:
            for index, item in enumerate(inputTOC):
                startTime = time.time()
                for checkField in ['type', 'name']:
                    if not checkField in item:
                        output["error"].append(f'"{checkField}" basic field not found: index={index}, item={item}')
                        continue

                if output["error"]:
                    return output

                if item['type'] not in ['chapter', 'imageDir', 'imagePdf']:
                    output["error"].append(f'"type" value error: index={index}, item={item}')
                    continue

                if item['type'] == 'chapter':
                    output['output'].append(item)

                elif item['type'] == 'imageDir':
                    """
                    {
                        "type": "imageDir",
                        "name": "name",
                        "imageDir": "/tmp/imageDir"
                    }
                    """
                    taskType = item['type']
                    checkFailed = False
                    for checkField in ['imageDir']:
                        if not checkField in item:
                            output["error"].append(f'type="{taskType}" error, "{checkField}" field not found: index={index}, item={item}')
                            checkFailed = False
                    if checkFailed:
                        continue
                    for pathCheck in ['imageDir']:
                        if not os.path.exists(item[pathCheck]):
                            output["error"].append(f'type="{taskType}" error, "{pathCheck}" not exists: index={index}, item={item}')
                            checkFailed = False
                    if checkFailed:
                        continue

                    images = common.getImagesFrom(item['imageDir'])
                    imageCount = len(images)
                    if imageCount == 0:
                        output["error"].append(f'type="imageDir" error, "imageDir" no images: index={index}, item={item}')
                        continue
                    output['totalImage'] += imageCount
                    output['output'].append(item)
                elif item['type'] == 'imagePdf':
                    """
                    {
                        "type": "imagePdf",
                        "name": "name",
                        "imagePdf": "/tmp/test.pdf",
                        "workDir": "/tmp/test.pdf/",
                        "imagePdfSaveFormat": "png",
                        "imagePdfSaveQuality": 100
                    }
                    """
                    taskType = item['type']
                    checkFailed = False
                    for checkField in ['imagePdf', 'workDir', 'imagePdfSaveFormat', 'imagePdfSaveQuality']:
                        if not checkField in item:
                            output["error"].append(f'type="{taskType}" error, "{checkField}" field not found: index={index}, item={item}')
                            checkFailed = True
                    if checkFailed:
                        continue
                    for pathCheck in ['imagePdf', 'workDir']:
                        if not os.path.exists(item[pathCheck]):
                            output["error"].append(f'type="{taskType}" error, "{pathCheck}" not exists: index={index}, item={item}')
                            checkFailed = True
                    if checkFailed:
                        continue
                    item['imagePdfSaveFormat'] = item['imagePdfSaveFormat'].lower()
                    if item['imagePdfSaveFormat'] not in ['jpg', 'png', 'gif']:
                            output["error"].append(f'type="{taskType}" error, "imagePdfSaveFormat" not supported (jpg, png, gif): index={index}, item={item}')
                            checkFailed = True
                    if checkFailed:
                        continue

                    try:
                        pdfDocument = fitz.open(item['imagePdf'])
                        totalImageCount = 0
                        for pageNumber in range(pdfDocument.page_count):
                            page = pdfDocument[pageNumber]
                            images = page.get_images(full=True)
                            for imgIndex, imgInfo in enumerate(images):
                                targetImage = pdfDocument.extract_image(imgInfo[0])
                                saveToPath = os.path.join(item['workDir'], f"{totalImageCount:03}.{item['imagePdfSaveFormat']}")
                                imageBytes, imageSize = common.convertImageQuality(targetImage['image'], item['imagePdfSaveFormat'], item['imagePdfSaveQuality'])
                                with open(saveToPath, "wb") as f:
                                    f.write(imageBytes)
                                totalImageCount += 1
                        
                        outputItem = {
                            'type': 'imageDir',
                            'name': item['name'],
                            'imageDir': item['workDir'],
                        }
                        for itemField in ['xhtmlTemplateId', 'autoBuildFirstPage', 'keepEvenNumberedPages']:
                            if itemField in item:
                                outputItem[itemField] = item[itemField]
                        output['output'].append(outputItem)
                        output['totalImage'] += totalImageCount
                    except Exception as e:
                        output["error"].append(f'type="{taskType}" pdf error: {e}')

                output['timeCost'].append(time.time() - startTime)

        output['status'] = len( output["error"]) == 0

        return output

    def setXHTMLStyle(self, cssFilename: str, styleContent: str):
        if 'style' not in self.xhtmlResource:
            self.xhtmlResource['style'] = {}
        self.xhtmlResource['style'][cssFilename] = styleContent

    def disableXHTMLStyle(self, cssFilename: str):
        if 'style' in self.xhtmlResource and cssFilename in self.xhtmlResource['style']:
            del self.xhtmlResource['style'][cssFilename]

    def setXHTMLTemplate(self, target: str, templateContent: str):
        if target and templateContent:
            self.xhtmlTemplate[target] = templateContent

    def enableImageFormatConversion(self, quality: int = 100, fromImageFormat: str = 'png', toImageFormat: str = 'jpg'):
        fromImageFormat = fromImageFormat.lower()
        toImageFormat = toImageFormat.lower()
        self.imageFormatConversionTable[ fromImageFormat ] = { 'to': toImageFormat , 'quality': quality }

    def disableImageFormatConversion(self, fromImageFormat: str):
        fromImageFormat = fromImageFormat.lower()
        if fromImageFormat in self.imageFormatConversionTable:
            del self.imageFormatConversionTable[fromImageFormat]

    def getObjectId(self, prefixName: str = 'id'):
        self.objectId += 1
        return f"{prefixName}-{self.objectId:06}"
 
    def createDefaultCover(self, backgroundColor: str = 'white', width: int = 600, height: int = 800, imageFormat: str = 'png'):
        defaultCover = Image.new('RGB', (width, height), color=backgroundColor)
        bookCoverBytes = BytesIO()
        imageFormat = imageFormat.lower()
        if imageFormat == 'png':
            self.bookCoverFilename = 'cover.png'
        elif imageFormat == 'jpg':
            self.bookCoverFilename = 'cover.jpg'
        defaultCover.save(bookCoverBytes, format=imageFormat)
        self.bookCoverBytes = bookCoverBytes.getvalue()
        return

    def setCover(self, imageBytes, imageFormat: str = 'png'):
        self.bookCoverBytes = imageBytes
        imageFormat = imageFormat.lower()
        if imageFormat == 'png':
            self.bookCoverFilename = 'cover.png'
        elif imageFormat == 'jpg' or imageFormat == 'jpeg':
            self.bookCoverFilename = 'cover.jpg'
        elif imageFormat == 'gif':
            self.bookCoverFilename = 'cover.gif'
        self.hasBookCover = True
    
    def setCoverByPath(self, imagePath: str, imageFormat: str = 'png') -> bool:
        if os.path.exists(imagePath):
            with open (imagePath, 'rb') as file:
                self.setCover(file.read(), imageFormat)
            return True
        return False

    def getCoverBytes(self):
        return self.bookCoverBytes

    def createNewChapter(self, chapterTitle: str, chapterId: str, chapterContent: str):
        chapterFilename = f"xhtml-{chapterId}.xhtml"
        obj = epub.EpubHtml(title=chapterTitle, file_name=chapterFilename, lang=self.bookLanguage, content=chapterContent)
        return (obj, chapterFilename, chapterId)

    def enableImageBookLayout(self):
        self.bookOpfMeta.append(
            {
                'namespace': None,
                'tag': 'meta',
                'value': 'pre-paginated',
                'others': {
                    'property': 'rendition:layout'
                }
            }
        )
        self.bookOpfMeta.append(
            {
                'namespace': None,
                'tag': 'meta',
                'value': 'landscape',
                'others': {
                    'property': 'rendition:spread'
                }
            }
        )

    def build(self):
        # create epub object
        book = epub.EpubBook()
        book.set_direction(self.bookPageProgressionDirection)
        book.set_identifier(self.bookId)
        book.set_title(self.bookTitle)
        book.set_language(self.bookLanguage)
        bookSpine = [] # ["nav"]
        bookTableOfContent = []

        if self.bookAuthor:
            for author in self.bookAuthor:
                book.add_author(author)

        # create a cover
        if self.bookCoverBytes != None:
            book.set_cover(self.bookCoverFilename, self.bookCoverBytes)

        if self.bookOpfMeta:
            for metaItem in self.bookOpfMeta:
                if 'value' not in metaItem or 'tag' not in metaItem:
                    continue
                book.add_metadata(
                    metaItem['namespace'] if 'namespace' in metaItem else None, 
                    metaItem['tag'], metaItem['value'],
                    metaItem['others'] if 'others' in metaItem else None
                )

        xhtmlResource = {}
        if self.xhtmlResource:
            if self.xhtmlResource['style']:
                for cssFileName, cssContent in self.xhtmlResource['style'].items():
                    cssObj = epub.EpubItem(uid=self.getObjectId(f'css'), file_name=cssFileName, content=cssContent, media_type='text/css')
                    book.add_item(cssObj)
                    xhtmlResource[cssFileName] = cssObj


        if self.tableOfContent:
            # import images
            for index, item in enumerate(self.tableOfContent):
                if 'type' not in item:
                    continue

                if item['type'] == 'article':
                    pass
                elif item['type'] == 'imageDir':
                    if 'imageDir' not in item:
                        continue
                    if 'name' not in item:
                        continue
                    images = common.getImagesFrom(item['imageDir'])
                    totalImages = len(images)
                    #pickFirstPage = False
                    for imageIndex, imageInfo in enumerate(images):
                        imagePath = imageInfo[0]
                        exname = imageInfo[1].strip().strip('.').lower()
                        filename = imageInfo[2] 
                        mediaType = 'image/png'
                        if exname == 'jpg':
                            mediaType = 'image/jpeg'
                        elif exname == 'gif':
                            mediaType = 'image/gif'
    
                        with open(imagePath, 'rb') as f:
                            imageSize = (0, 0)
                            imageData = f.read()
                            imageUid = self.getObjectId(f'img-{index + 1}')
                            imageOutputPath = f"{imageUid}.{exname}"
                            if exname in self.imageFormatConversionTable:
                                imageSetup = self.imageFormatConversionTable[exname]
                                imageData, imageSize = common.convertImageQuality(imageData, imageSetup['to'], imageSetup['quality'])
                                imageOutputPath = f"{imageUid}.{imageSetup['to']}"
                            else:
                                imageSize = common.getImageSize(imageData)
                            imageObj = epub.EpubImage(uid=imageUid, file_name=imageOutputPath, media_type=mediaType, content=imageData)
                            if not self.hasBookCover and self.pickFirstImageToBeBookCover:
                                self.setCover(imageData, common.getImageBytesFormat(imageData))
                                if self.bookCoverBytes != None:
                                    book.set_cover(self.bookCoverFilename, self.bookCoverBytes)

                            book.add_item(imageObj)
                            chapterUid = self.getObjectId(f'{index + 1}')
                            if imageIndex % 20 == 0:
                                chapterTitle = f'{item["name"]} - {imageIndex+1:04} / {totalImages:04} {(imageIndex + 1) * 100/totalImages:.2f}%'
                            else:
                                chapterTitle = f'{item["name"]} - {imageIndex+1:04}'

                            chapterObj, chapterFilename, chapterId = self.createNewChapter(
                                chapterTitle,
                                chapterUid,
                                self.xhtmlTemplate["image"].format(
                                    imageName=imageOutputPath, 
                                    imageWidth=imageSize[0],
                                    imageHeight=imageSize[1],
                                    imageTitle=imageOutputPath,
                                    imagePath=imageOutputPath
                                )
                            )

                            #chapterObj.add_property('svg')
                            chapterObj.add_meta(name='viewport', content=f'width={imageSize[0]}, height={imageSize[1]}')

                            if xhtmlResource:
                                for cssName, itemResource in xhtmlResource.items():
                                    chapterObj.add_item(itemResource)

                            #print(chapterObj.get_body_content())
                            book.add_item(chapterObj)
                            bookSpine.append(chapterObj)

                            #if pickFirstPage:
                            #    pickFirstPage = False
                            #    bookTableOfContent.append( chapterObj )
                            bookTableOfContent.append( chapterObj )


        book.spine = bookSpine
        book.toc = tuple(bookTableOfContent)
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        epub.write_epub(self.outputEPUBPath, book, {})

        return self.outputEPUBPath

