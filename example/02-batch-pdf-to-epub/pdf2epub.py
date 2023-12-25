import os
import sys
import json
import subprocess
import tempfile

from epub_image_helper.common import loadBookInfoFromConfigOfPdfs, exampleGetBookStorageInfoFromPdfsFunc

if __name__ == '__main__':
    inputList = 'input.json'
    outputResult = 'epub'
    if not os.path.exists(outputResult):
        print(f"output `{outputResult}` not found. Please mkdir `{outputResult}` first ")
        sys.exit(0)

    todoTask = []
    inputData = loadBookInfoFromConfigOfPdfs(inputList, getBookStorageInfoFunc=exampleGetBookStorageInfoFromPdfsFunc)

    for item in inputData:
        print(f"{item['name']}, count: {len(item['books'])}")
        outputDir = os.path.join(outputResult, item['name'])
        for bookIndex, bookInfo in enumerate(item['books']):
            bookName = os.path.basename(bookInfo['file']).rsplit('.', 1)[0]
            todoTask.append({
                'name': bookName,
                'type': 'imagePdf',
                'imagePdf': bookInfo['storage'],
                'outputDir': outputDir,
                'output': os.path.join(outputDir, f"{bookName}.epub"),
            })
    print(json.dumps(todoTask))
    #sys.exit(0)
    for task in todoTask:
        print(task)
        try:
            if not os.path.exists(task['outputDir']):
                os.makedirs(task['outputDir'])
        except Exception as e:
            print(f'Error: {e}')
            sys.exit(0)

        if os.path.exists(task['output']):
            continue

        taskCommand = [
            'epub-image-helper', 
            '--bookConfig', '@-' ,
            '--enableImageBookLayout',
        ]
        f = tempfile.TemporaryDirectory(dir='/tmp', prefix='___')
        if True:
            tmpWorkDir = f.name
            commandInput = json.dumps({
                'output': task['output'],
                'bookPageProgressionDirection': 'rtl',
                'enableImageBookLayout': True,
                'pickFirstImageToBeBookCover': True,
                'imageFormatConversionTable': {
                    #'png': { 'to': 'jpg', 'quality': 85},
                },
                'bookTitle': task['name'],
                'bookTableOfContent': [
                    {
                        'type': 'imagePdf',
                        'name': task['name'],
                        'imagePdf': task['imagePdf'],
                        'imagePdfSaveFormat': 'png',
                        'imagePdfSaveQuality': 100,
                        'workDir': tmpWorkDir,
                    }
                ],
            })
            taskCommand = ' '.join(taskCommand)
            process = subprocess.Popen(taskCommand, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            commandOutput, error = process.communicate(input=commandInput)
            print(commandOutput)
            print(error)
