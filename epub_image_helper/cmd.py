# -*- encoding: utf-8 -*-
import os
import sys
import argparse
import datetime
import subprocess
import json
import uuid
import time

from epub_image_helper import __version__
from epub_image_helper import common
from epub_image_helper import epubImageHelper

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("imageDir", nargs="*", type=str, help="the directory where the image file is located")
    parser.add_argument("--output", type=str, default='/tmp/test.epub', help="output epub path")
    parser.add_argument("--bookConfig", type=str, default='{}', help="a JSON config for EPUB builder. '@-' will read from stdin")
    parser.add_argument("--bookCover", type=str, default='', help="set a cover image for EPUB")
    parser.add_argument("--bookTitle", type=str, default='Unknown', help="set book title")
    parser.add_argument("--bookId", type=str, default=str(uuid.uuid4()), help="set book uuid info")
    parser.add_argument("--bookAuthor", type=str, default='Unknown', help="set book author info")
    parser.add_argument("--pickFirstImageToBeBookCover", action="store_true", default=False, help="Select the first image as the book cover when the 'bookCover' parameter is not specified")
    parser.add_argument("--debug", action="store_true", default=False, help="show bookConfig only")
    parser.add_argument("--epubcheck", action="store_true", default=False, help="test output epub format via epubcheck command")

    args = parser.parse_args()

    startTime = time.time()

    output = { 'status': False, 'input': {}, 'output': { 'path': None, 'size': 0, 'sizeReadable': None, 'imageCount': 0, 'timeCost': []} , 'error': [] , 'version': __version__ }

    output['input']['output'] = args.output
    output['input']['bookConfig'] = args.bookConfig
    output['input']['bookCover'] = args.bookCover
    output['input']['bookId'] = args.bookId
    output['input']['bookTitle'] = args.bookTitle
    output['input']['bookAuthor'] = args.bookAuthor
    output['input']['epubcheck'] = args.epubcheck
    output['input']['imageDir'] = args.imageDir
    output['input']['pickFirstImageToBeBookCover'] = args.pickFirstImageToBeBookCover
    output['input']['debug'] = args.debug
    output['input']['bookTableOfContent'] = []
    output['input']['imageFormatConversionTable'] = {}

    bookConfig = output['input']['bookConfig']
    if output['input']['bookConfig'] == '@-':
        output['input']['stdin'] = ''
        bookConfigJSONObject = None
        for line in sys.stdin:
            output['input']['stdin'] += line
        bookConfig = output['input']['stdin']

    if bookConfig:
        try:
            bookConfigJSONObject = json.loads(bookConfig)
        except json.JSONDecodeError as e:
            output['error'].append(f'input bookConfig json decode error: {e}')
            print(json.dumps(output, indent=4))
            sys.exit(0)

        if bookConfigJSONObject:
            for field in ['bookCover', 'bookId', 'bookAuthor', 'epubcheck', 'bookTableOfContent', 'imageDir', 'pickFirstImageToBeBookCover', 'debug', 'imageFormatConversionTable']:
                if field in bookConfigJSONObject:
                    output['input'][field] = bookConfigJSONObject[field]

            if type(output['input']['imageDir']) is not list:
                output['input']['imageDir'] = [output['input']['imageDir']]

    if not output['input']['bookTableOfContent'] and not output['input']['imageDir']: 
        output['error'].append("If both 'imageDir' and 'bookTableOfContent' are empty, please set at least one of them.")
    else:
        for item in output['input']['imageDir']:
            if not os.path.exists(item):
                output['error'].append(f'imageDir: [{item}] is not found')
                continue
            try:
                with os.scandir(item):
                    pass
                output['input']['bookTableOfContent'].append(
                    {'type': 'imageDir', 'name': os.path.basename(item) or os.path.basename(os.path.dirname(item)), 'imageDir': item}
                )
            except:
                output['error'].append(f'imageDir: [{item}] is not readable')

    if output['input']['imageFormatConversionTable']:
        for fromImageFormat, imageSetup in output['input']['imageFormatConversionTable'].items():
            if 'to' not in imageSetup:
                output['error'].append(f'check imageFormatConversionTable: {imageSetup} no to')
            if 'quality' not in imageSetup:
                output['error'].append(f'check imageFormatConversionTable: {imageSetup} no quality')

    if output['input']['bookCover']:
        if not os.path.exists(output['input']['bookCover']):
            output['error'].append(f"check bookCover failed: {output['input']['bookCover']} not found")

    output['output']['timeCost'].append(time.time() - startTime)

    if len(output['error']) > 0:
        print(json.dumps(output, indent=4))
        sys.exit(0)

    startTime = time.time()

    obj = epubImageHelper.EPUBImageHelper(
        outputEPUBPath=output['input']['output'], 
        imageBookId=output['input']['bookId'],
        imageBookTitle=output['input']['bookTitle'],
        imageBookAuthor=output['input']['bookAuthor'],
        #tableOfContent=output['input']['bookTableOfContent']
        pickFirstImageToBeBookCover=output['input']['pickFirstImageToBeBookCover'], 
    )

    if output['input']['bookTableOfContent']:
        setTOCStatus = obj.setTableOfContent(output['input']['bookTableOfContent'])
        if setTOCStatus['status'] == False:
            output['error'].append(setTOCStatus)
        elif setTOCStatus['totalImage'] == 0:
            output['error'].append('no input images')
            output['error'].append(setTOCStatus)

    output['output']['timeCost'].append(time.time() - startTime)

    if len(output['error']) > 0:
        print(json.dumps(output, indent=4))
        sys.exit(0)

    if output['input']['bookCover'] and os.path.exists(output['input']['bookCover']):
        checkFilenameEx = output['input']['bookCover'].lower()
        imageFormat = 'png'
        if checkFilenameEx.endswith('.jpg') or checkFilenameEx.endswith('.jpeg'):
            imageFormat = 'jpg'
        elif checkFilenameEx.endswith('.gif'):
            imageFormat = 'gif'
        obj.setCoverByPath(output['input']['bookCover'], imageFormat)
    
    if output['input']['imageFormatConversionTable']:
        for fromImageFormat, imageSetup in output['input']['imageFormatConversionTable'].items():
            obj.enableImageFormatConversion(int(imageSetup['quality']), fromImageFormat, imageSetup['to'])

    if output['input']['debug']:
        print(json.dumps(output, indent=4))
        sys.exit(0)

    startTime = time.time()
    output['output']['path'] = obj.build()
    output['output']['timeCost'].append(time.time() - startTime)
    try:
        output['output']['size'] = os.path.getsize(output['output']['path'])
        output['output']['sizeReadable'] = common.getFileSizeReadable(output['output']['size'])
    except Exception as e:
        pass
    output['status'] = output['output']['size'] > 0
    if output['status'] and output['input']['epubcheck']:
        startTime = time.time()
        output['verify'] = { 'status': False, 'command': [ "epubcheck", output['output']['path'], "--json", "-"], "stdout": None, "stderr": None, "error": None}
        try:
            result = subprocess.run(output['verify']['command'], capture_output=True, text=True)
            try:
                output['verify']['stderr'] = result.stderr.strip()
                if len(output['verify']['stderr']) == 0:
                    output['verify']['status'] = True
                output['verify']['stdout'] = json.loads("\n".join(result.stdout.split("\n")[1:]))
            except json.JSONDecodeError as e:
                output['verify']['error'] = f"JSON decoding failed with error: {e}"
        except subprocess.CalledProcessError as e:
            output['verify']['error'] = str(e.output)
        except Exception as e:
            output['verify']['error'] = str(e)
        output['output']['timeCost'].append(time.time() - startTime)
        output['status'] = output['verify']['status']
    print(json.dumps(output, indent=4))

if __name__ == '__main__':
    main()
