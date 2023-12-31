# -*- coding: utf-8 -*-
import os
from PIL import Image
from io import BytesIO
import re
import sys
import json
import hashlib
from urllib.parse import urlparse

def getFileSizeReadable(size: int):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unitIndex = 0
    while size >= 1024 and unitIndex < len(units) - 1:
        size /= 1024.0
        unitIndex += 1
    return f"{size:.2f} {units[unitIndex]}"

def getImageSize(imageBytes):
    objImage = Image.open(BytesIO(imageBytes))
    return objImage.size

def getImageBytesFormat(imageBytes):
    try:
        with Image.open(BytesIO(imageBytes)) as img:
            return img.format.lower()
    except Exception as e:
        pass
    return None

def convertImageQuality(imageBytes, toImageFormat: str = 'png', quality: int = 100):
    if not imageBytes:
        return None

    objImage = Image.open(BytesIO(imageBytes))
    imageBuffer = BytesIO()
    toImageFormat = toImageFormat.lower()

    #print(f'convertImageQuality: mode={objImage.mode}, format={objImage.format.lower()}, toImageFormat={toImageFormat}, quality={quality}')

    if quality == 100:
        if objImage.format.lower() == toImageFormat:
            return (imageBytes, objImage.size)

    if objImage.mode != 'RGB':
        #print(f'use RGB: {objImage.size}')
        objImage = objImage.convert("RGB")
    if toImageFormat == 'jpg' or toImageFormat == 'jpeg':
        #print(f'to jpg: {objImage.size}, quality: {quality}')
        objImage.save(imageBuffer, "JPEG", quality=quality)
    elif  toImageFormat == 'png':
        #print(f'to png: {objImage.size}, quality: {quality}')
        objImage.save(imageBuffer, "PNG", quality=quality)
    elif  toImageFormat == 'gif':
        #print(f'to gif: {objImage.size}, quality: {quality}')
        objImage.save(imageBuffer, "GIF", quality=quality)
    return (imageBuffer.getvalue(), objImage.size)

def convertPNGToJPGInMemory(pngBytes, quality: int = 100):
    pngImage = Image.open(BytesIO(pngBytes))
    jpgBuffer = BytesIO()
    if pngImage.mode != 'RGB':
        pngImage = pngImage.convert("RGB")
    pngImage.save(jpgBuffer, "JPEG", quality=quality)
    jpgBytes = jpgBuffer.getvalue()
    return jpgBytes

def convertPNGFileToJPGFile(outputJPGPath: str, pngPath: str, quality: int = 100):
    pngImage = Image.open(pngPath)
    if pngImage.mode != 'RGB':
        pngImage = pngImage.convert("RGB")
    pngImage.save(outputJPGPath, "JPEG", quality=quality)

def getImagesFrom(path: str, extension: list[str] = ['.png', '.jpg', '.gif'], sortByFilename: bool = True) -> list[str]:
    output = []
    extension = [ exname.lower() for exname in extension]
    if path and os.path.exists(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if not extension:
                    output.append((os.path.join(root, file), '', file))
                    continue
                for exname in extension:
                    if file.lower().endswith(exname):
                        output.append((os.path.join(root, file), exname, file))
                        break
        if sortByFilename:
            output.sort()
    return output

def exampleGetBookStorageInfoFromUrlsFunc(bookUrl):
    # build a bookRawId from URL
    bookRawId = hashlib.md5(bookUrl.encode()).hexdigest()
    match = re.search(r'/(\d+)/', bookUrl)
    if match:
        bookRawId = match.group(1)
    return os.path.join('storage', 'url', bookRawId)

def exampleGetBookStorageInfoFromPdfsFunc(bookPath):
    return os.path.join('storage', 'pdf', bookPath)

def loadBookInfoFromConfigOfUrls(inputJsonPath = 'input.json', getBookStorageInfoFunc = None):
    output = []
    if not getBookStorageInfoFunc or not callable(getBookStorageInfoFunc):
        print(f"getBookStorageInfoFunc not found or getBookStorageInfoFunc is not callable func")
        return output
    try:
        with open(inputJsonPath, 'r') as file:
            rawJson = json.load(file)
            for item in rawJson:
                if 'name' not in item or not item['name']:
                    continue
                if 'books' not in item or not item['books']:
                    continue
                books = []
                for bookId, bookURL in enumerate(item['books']):
                    bookImageStoragePath = getBookStorageInfoFunc(bookURL)
                    # A flag to determine whether to convert to epub
                    if not os.path.exists(bookImageStoragePath):
                        continue
                    outItem = {
                        "id": bookId, "url": bookURL, 'storage': bookImageStoragePath,
                    }
                    if 'author' in item:
                        outItem['author'] = item['author']
                    books.append(outItem)
                if books:
                    output.append({ "name": item['name'], "books": books })
    except FileNotFoundError:
        print(f"inputJson.json: {inputJsonPath} not found")
    except json.JSONDecodeError:
        print(f"inputJson.json: {inputJsonPath} not json format")
    return output

def loadBookInfoFromConfigOfPdfs(inputJsonPath = 'input.json', getBookStorageInfoFunc = None):
    output = []
    if not getBookStorageInfoFunc or not callable(getBookStorageInfoFunc):
        print(f"getBookStorageInfoFunc not found or getBookStorageInfoFunc is not callable func")
        return output
    try:
        with open(inputJsonPath, 'r') as file:
            rawJson = json.load(file)
            for item in rawJson:
                if 'name' not in item or not item['name']:
                    continue
                if 'books' not in item or not item['books']:
                    continue
                books = []
                for bookId, bookPDFPath in enumerate(item['books']):
                    bookImageStoragePath = getBookStorageInfoFunc(bookPDFPath)
                    # A flag to determine whether to convert to epub
                    if not os.path.exists(bookImageStoragePath):
                        continue
                    outItem = {
                        "id": bookId, "file": bookPDFPath, 'storage': bookImageStoragePath,
                    }
                    if 'author' in item:
                        outItem['author'] = item['author']
                    books.append(outItem)
                if books:
                    output.append({ "name": item['name'], "books": books })
    except FileNotFoundError:
        print(f"inputJson.json: {inputJsonPath} not found")
    except json.JSONDecodeError:
        print(f"inputJson.json: {inputJsonPath} not json format")
    return output

