#!/usr/bin/env python
import pyamf
import pyamf.xml
from pyamf import remoting
from etree import ElementTree
pyamf.xml.set_default_interface(ElementTree)
import httplib
import urllib2
from amf import BrightCoveAMFHelper
import sys

# from plugin.video.catchuptv.au.ten/resources/lib/networktenvideo/api.py
API_TOKEN = 'lWCaZyhokufjqe7H4TLpXwHSTnNXtqHxyMvoNOsmYA_GRaZ4zcwysw..'
PLAYER_KEY = 'AQ~~,AAACAC_zRoE~,GmfXBj8vjuSBlqMYKWGHoiljZL-ccjXh'
AMF_SEED = 'f94a0d8cf273ee668a1d9b7e6b7053148fb54065'
SWF_URL = 'http://admin.brightcove.com/viewer/us20130702.1553/connection/ExternalConnection_2.swf'
PAGE_URL = 'http://tenplay.com.au/'

def main(vars):
    if len(vars) > 1:
        try:
            videoId = str(int(vars[1]))
        except ValueError:
            videoId = urllib2.urlopen(vars[1]).read().split('videoID: "')[1].split('",')[0]
        amfHelper = BrightCoveAMFHelper(PLAYER_KEY, videoId, PAGE_URL, AMF_SEED)
        print amfHelper.data["IOSRenditions"][0]["defaultURL"]
        return 0
    else:
        return 1        

if __name__ == "__main__":
    sys.exit(main(sys.argv))
