import os
from PIL import Image
from io import BytesIO
from epub_image_helper.common import convertImageQuality

def testImageCompression(intputImageDir='/tmp/test-images'):
    if not os.path.exists(intputImageDir):
        print(f'"{intputImageDir}" not found')
        return

    for root, dirs, files in os.walk(intputImageDir):
        for file in files:
            for exname in ['jpg', 'png']:
                if file.lower().endswith(exname):
                    print(file)
                    with open(os.path.join(root, file), 'rb') as f:
                        rawData = f.read()
                        for plan in [ 
                                {'to': 'png', 'quality': 100}, 
                                {'to': 'png', 'quality': 95}, 
                                {'to': 'png', 'quality': 90}, 
                                {'to': 'png', 'quality': 85}, 
                                {'to': 'jpg', 'quality': 100} ,
                                {'to': 'jpg', 'quality': 95} ,
                                {'to': 'jpg', 'quality': 90} ,
                                {'to': 'jpg', 'quality': 85} ,
                            ]:
                            newData, _ = convertImageQuality(rawData, plan['to'], plan['quality']) 

                            print(f"plan: {plan['to']}, {plan['quality']}: rawSize: {len(rawData)}, newSize: {len(newData)}" )
