import json
import subprocess

def testPdf2Epub(inputFile='/tmp/input.pdf', outputFile='/tmp/output.epub', tmpWorkDir='/tmp/test-pdf-workdir'):
    taskCommand = [
        'epub-image-helper', 
        '--bookConfig', '@-' ,
        '--enableImageBookLayout',
    ]
    commandInput = json.dumps({
        'output': outputFile,
        'bookPageProgressionDirection': 'rtl',
        'enableImageBookLayout': True,
        'pickFirstImageToBeBookCover': True,
        'imageFormatConversionTable': {
            #'png': { 'to': 'jpg', 'quality': 85},
        },
        'bookTitle': 'HelloWorld',
        'bookTableOfContent': [
            {
                'type': 'imagePdf',
                'name': 'Hello',
                'imagePdf': inputFile,
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

