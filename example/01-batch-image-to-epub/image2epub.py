import os
import sys
import json
import subprocess

from epub_image_helper.common import loadBookInfoFromConfigOfUrls, exampleGetBookStorageInfoFromUrlsFunc

if __name__ == '__main__':
    inputList = 'input.json'
    outputResult = 'epub'
    if not os.path.exists(outputResult):
        print(f"output `{outputResult}` not found. Please mkdir `{outputResult}` first ")
        sys.exit(0)

    todoTask = []
    inputData = loadBookInfoFromConfigOfUrls(inputList, getBookStorageInfoFunc=exampleGetBookStorageInfoFromUrlsFunc)
    for item in inputData:
        print(f"{item['name']}, count: {len(item['books'])}")
        outputDir = os.path.join(outputResult, item['name'])
        for bookIndex, bookInfo in enumerate(item['books']):
            bookName = f"{item['name']}{bookIndex+1:02}" if len(item['books']) != 1 else item['name']
            todoTask.append({
                'name': bookName,
                'type': 'imageDir',
                'author': bookInfo['author'],
                'imageDir': bookInfo['storage'],
                'outputDir': outputDir,
                'output': os.path.join(outputDir, f"{bookName}.epub"),
            })
    print(json.dumps(todoTask))
    for task in todoTask:
        print(task)
        try:
            if not os.path.exists(task['outputDir']):
                os.makedirs(task['outputDir'])
        except Exception as e:
            print(f'Error: {e}')
            sys.exit(0)

        if os.path.exists(task['output']):
            print(f"Done: {task['output']}")
            continue

        taskCommand = [
            'epub-image-helper', 
            '--bookConfig', '@-' ,
            '--enableImageBookLayout',
        ]
        commandInput = json.dumps({
            'output': task['output'],
            'bookPageProgressionDirection': 'rtl',
            'bookAuthor': task['author'],
            'enableImageBookLayout': True,
            'pickFirstImageToBeBookCover': True,
            'imageFormatConversionTable': {
                'png': { 'to': 'jpg', 'quality': 95},
            },
            'bookTitle': task['name'],
            'bookTableOfContent': [
                {
                    'type': 'imageDir',
                    'name': task['name'],
                    'imageDir': task['imageDir'],
                }
            ],
        })
        taskCommand = ' '.join(taskCommand)
        process = subprocess.Popen(taskCommand, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        commandOutput, error = process.communicate(input=commandInput)
        print(commandOutput)
        print(error)
