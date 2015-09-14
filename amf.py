#
#   Network Ten CatchUp TV Video API Library
#
#   Copyright (c) 2013 Adam Malcontenti-Wilson
# 
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
# 
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
# 
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#   THE SOFTWARE.
#
#   Portions of this code are from http://boxee.bartsidee.nl/repo/sbs6/sbs6.py
#

import httplib
import pyamf
import pyamf.xml
from pyamf import remoting
from etree import ElementTree

pyamf.xml.set_default_interface(ElementTree)

class BrightCoveAMFHelper:
    """ BrightCoveHelper is used to get video info of videos that use the 
    BrightCover SWF player.
        
    """
    
    def __init__(self, playerKey, contentId, url, seed, experienceId=0, amfVersion=3):
        """ Initializes the BrightCoveHelper """
        
        self.playerKey = playerKey
        self.contentId = contentId
        self.url = url
        self.seed = seed
        self.experienceId = experienceId
        self.amfVersion = amfVersion
        
        self.logger = False
        self.data = self.__GetBrightCoveData()
        return
    
    def GetStreamInfo(self):
        """ Returns the streams in the form of a list of 
        tuples (streamUrl, bitrate).
        
        """
        
        streams = []
        streamData = self.data['renditions']
        for stream in streamData:
            bitrate = int(stream['encodingRate'])/1000
            # The result is Unicode, so we should encode it.
            strm = stream['defaultURL']
            streams.append((strm, bitrate))
            
        return streams
    
    def __GetBrightCoveData(self):
        """ Retrieves the Url's from a brightcove stream
        
        Arguments:
        playerKey : string - Key identifying the current request
        contentId : int    - ID of the content to retrieve
        url       : string - Url of the page that calls the video SWF
        seed      : string - Constant which depends on the website
        
        Keyword Arguments:
        experienceId : id     - <unknown parameter>
        
        Returns a dictionary with the data
        
        """
        
        # Seed = 61773bc7479ab4e69a5214f17fd4afd21fe1987a
        envelope = self.__BuildBrightCoveAmfRequest(self.playerKey, self.contentId, self.url, self.experienceId, self.seed)
        
        connection = httplib.HTTPConnection("c.brightcove.com")
        connection.request("POST", "/services/messagebroker/amf?playerKey="+self.playerKey, str(remoting.encode(envelope).read()),{'content-type': 'application/x-amf'})
        response = connection.getresponse().read()
        response = remoting.decode(response).bodies[0][1].body
        
        #self.logger.debug(response)     
        return response['programmedContent']['videoPlayer']['mediaDTO']       
    
    def __BuildBrightCoveAmfRequest(self, playerKey, contentId, url, experienceId, seed):
        """ Builds a AMF request compatible with BrightCove
        
        Arguments:
        playerKey : string - Key identifying the current request
        contentId : int    - ID of the content to retrieve
        url       : string - Url of the page that calls the video SWF 
        seed      : string - Constant which depends on the website
        
        Keyword Arguments:
        experienceId : id     - <unknown parameter>
        
        Returns a valid Brightcove request
        
        """
        
        #const = '686a10e2a34ec3ea6af8f2f1c41788804e0480cb'
        pyamf.register_class(ViewerExperienceRequest, 'com.brightcove.experience.ViewerExperienceRequest')
        pyamf.register_class(ContentOverride, 'com.brightcove.experience.ContentOverride')
        
        contentOverrides = [ContentOverride(int(contentId))]
        viewerExperienceRequest = ViewerExperienceRequest(url, contentOverrides, int(experienceId), playerKey)
    
        envelope = remoting.Envelope(amfVersion=self.amfVersion)
        remotingRequest = remoting.Request(target="com.brightcove.experience.ExperienceRuntimeFacade.getDataForExperience",body=[seed, viewerExperienceRequest],envelope=envelope)
        envelope.bodies.append(("/1", remotingRequest))
        
        return envelope

class ViewerExperienceRequest(object):
    """ Class needed for brightcove AMF requests """
    def __init__(self, URL, contentOverrides, experienceId, playerKey, TTLToken=''):
        self.TTLToken = TTLToken
        self.URL = URL
        self.deliveryType = float(0)
        self.contentOverrides = contentOverrides
        self.experienceId = experienceId
        self.playerKey = playerKey

class ContentOverride(object):
    """ Class needed for brightcove AMF requests """
    def __init__(self, contentId, contentType=0, target='videoPlayer'):
        self.contentType = contentType
        self.contentId = contentId
        self.target = target
        self.contentIds = None
        self.contentRefId = None
        self.contentRefIds = None
        self.contentType = 0
        self.featureId = float(0)
        self.featuredRefId = None
