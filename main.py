import webapp2, urllib, urllib2, webbrowser
import jinja2

import os
import logging

import json


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)



class MainHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("In MainHandurler")
        template_values = {}

        template_values['page_title'] = "Ski Resort Search"
        template = JINJA_ENVIRONMENT.get_template('greetform.html')
        self.response.write(template.render(template_values))


def safeGet(url):
    try:
        return urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        print 'The server couln\'t fulfill the request.'
        print 'Error code: ', e.code
    except urllib2.URLError, e:
        print 'We failed to reach a server'
        print 'Reason: ', e.reason
    return None

paramstr = urllib.urlencode({'format': 'json'})

def getTriplet(Name):
    baseurl = 'http://api.powderlin.es/stations'
    allSkiResortRequest = baseurl + '?' + paramstr
    logging.info(allSkiResortRequest)
    r = urllib2.urlopen(allSkiResortRequest)
    allskijsonstr = r.read()
    allskiResortData = json.loads(allskijsonstr)
    for x in allskiResortData:
        if Name.upper() in x['name']:
            return (x['triplet'])

def getSkiResort(skiResortName):
    if getTriplet(skiResortName) == None:
        return None
    else:
        code = getTriplet(skiResortName)
    basicurl = 'http://api.powderlin.es/station/'
    skiurl = basicurl + code + '?' + paramstr
    skiopen = urllib2.urlopen(skiurl)
    skiread = skiopen.read()
    codedata = json.loads(skiread)
    return codedata

accesscode = "dcc2f0f5-e88f-4c68-a94d-257765e86d95"

#Camera Image data
def CameraRest():
    basicurl = 'http://wsdot.com/Traffic/api/HighwayCameras/HighwayCamerasREST.svc/GetCamerasAsJson'
    paramstr = urllib.urlencode({'ACCESSCODE': accesscode})
    allCameraRequest = basicurl + '?'+ paramstr
    cameraOpen = urllib2.urlopen(allCameraRequest)
    cameraRead = cameraOpen.read()
    cameraDic = json.loads(cameraRead)
    return cameraDic


def getCameraImage(tag = "Stevens Pass"):
    myList = []
    for everyCamera in CameraRest():
        logging.info(everyCamera)
        if tag.lower() in everyCamera['Title'].lower():
            myList.append(everyCamera['ImageURL'])
    return myList

class SkiResort():
    def __init__(self, dic):
        self.name = dic['station_information']['name']
        self.dateInfo = {}
        for everyday in dic['data']:
            date = everyday['Date']
            temp = everyday['Observed Air Temperature (degrees farenheit)']
            if everyday['Snow Depth (in)'] == None:
                depth = "25"
            else:
                depth = everyday['Snow Depth (in)']
            self.dateInfo[date] = {"temp": temp, "depth": depth}


    def __str__(self):
        return "Ski Resort Name: %s \n Date: %s" % (self.name, self.dateInfo)

class GreetResponseHandlr(webapp2.RequestHandler):
    def post(self):
        vals = {}
        tag = self.request.get('tag')
        vals['page_title'] = "Search Results: "

        if tag:
            tag = self.request.get('tag')
            vals['tag'] = tag
            resorts = getSkiResort(tag)

            imageURL = getCameraImage(tag)

            ski_resort = SkiResort(resorts)

            vals['imageURL'] = imageURL
            vals['name'] = ski_resort.name
            vals['dateInfo'] = ski_resort.dateInfo

            template = JINJA_ENVIRONMENT.get_template('greetresponse.html')
            self.response.write(template.render(vals))
        else:
            template = JINJA_ENVIRONMENT.get_template('greetform.html')
            self.response.write(template.render(vals))



application = webapp2.WSGIApplication([ \
    ('/gresponse', GreetResponseHandlr),
    ('/.*', MainHandler)
],
    debug=True)