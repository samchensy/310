import urllib, urllib2, webbrowser


import json
# http://wsdot.com/Traffic/api/HighwayCameras/HighwayCamerasREST.svc/GetCamerasAsJson?AccessCode={ACCESSCODE}

accesscode = "dcc2f0f5-e88f-4c68-a94d-257765e86d95"


def CameraRest():
    basicurl = 'http://wsdot.com/Traffic/api/HighwayCameras/HighwayCamerasREST.svc/GetCamerasAsJson'
    paramstr = urllib.urlencode({'ACCESSCODE': accesscode})
    allCameraRequest = basicurl + '?'+ paramstr
    cameraOpen = urllib2.urlopen(allCameraRequest)
    cameraRead = cameraOpen.read()
    cameraDic = json.loads(cameraRead)
    return cameraDic

def getCameraImage(tag = "Snoqualmie Summit"):
    myList = []
    for everyCamera in CameraRest():
        if tag in everyCamera['Title']:
            myList.append(everyCamera['ImageURL'])
    return myList

print (getCameraImage())

