# DescribeIt: An Add-on for nvda that provides description of web images using Microsoft cognitive API 
#Copyright (C) 2016-2017 Assistech Lab IIT Delhi, Manshul Belani, Dinesh Kaushal
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import urllib2, urllib
import httplib, base64
import json
import ui
import textInfos
from logHandler import log
from urlparse import urlparse,urljoin
import treeInterceptorHandler
import configobj
import thread
import math
import scriptHandler
import api
import os
import globalVars

class imageDescription():
    def script_getImageDescription(self, gesture):
        obj=api.getFocusObject()
        treeInterceptor=obj.treeInterceptor
        if isinstance(treeInterceptor,treeInterceptorHandler.DocumentTreeInterceptor) and not treeInterceptor.passThrough:
            obj=treeInterceptor
            try:
                info=obj.makeTextInfo(textInfos.POSITION_CARET)
            except (NotImplementedError, RuntimeError):
                info=obj.makeTextInfo(textInfos.POSITION_FIRST)
            browseObj=info.NVDAObjectAtStart
        docHandle,ID=treeInterceptor.getIdentifierFromNVDAObject(browseObj)
        attrs=treeInterceptor.makeTextInfo(browseObj)._getControlFieldAttribs(docHandle,ID)
        if (attrs.get('HTMLAttrib::src',"")):
            imageUrl=str(attrs['HTMLAttrib::src'])
        else:
            weblink=obj._get_documentConstantIdentifier()
            imageUrl=str(urljoin(weblink,attrs['IAccessible2::attribute_src']))
        if imageUrl:
            try:
                thread.start_new_thread( self.getImageDescription, (imageUrl,) )
            except Exception as e:
                pass
    script_getImageDescription.category = _("imageDescription")
    
    def getResponse(self,proxyIP,proxyPort,uri_base,params,body,headers):
		try:
 			if proxyIP and proxyPort:
				conn = httplib.HTTPSConnection(proxyIP,proxyPort)
				conn.set_tunnel(uri_base,443)
 			else:
				conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
			conn.request("POST", "/vision/v1.0/analyze?%s" % params, str(body), headers)
			response = conn.getresponse()
			return response
		except Exception as e:
			# Translators: a message when unsuccessful connection with API
			ui.message(_("Could not connect to API"))
			log.debugWarning("Error connecting to API : %s" %e)
		conn.close()
        
    def extractDataFromResponse(self,response):
		dataMap={}
		data = response.read()
		# 'data' contains the JSON data. The following formats the JSON data for display.
		parsed = json.loads(data)
		data=json.loads(data)
		try:
			dscr=data['description']
			s=dscr['captions']
			s1=s[0]
			# Translators: to display result of API
			dataMap['description']=_(s1['text'])
			dataMap['confidence']=_(str((round(s1['confidence'],2))*100))
			color=data['color']
			dataMap['fgColor']=_(color['dominantColorForeground'])
			dataMap['bgColor']=_(color['dominantColorBackground'])
		except Exception as e:
			# Translators: a message when API is not able to return a description for image on web page
			ui.message(_(data['message']))
			log.debugWarning("Error- %s: %s",type(e),e)
			log.debugWarning("Error Message from API- %s: %s " ,data['code'], data['message'])
		return dataMap
        
    def getImageDescription(self,imageUrl):
		config = configobj.ConfigObj(os.path.join(globalVars.appArgs.configPath, "addons\DescribeIt\globalPlugins\DescribeIt\userDetails.ini" ))
		proxyIP=config.get('Proxy IP')
		proxyPort=config.get('Proxy Port')
		subscriptionKey=config.get('Key')
		uri_base = 'westcentralus.api.cognitive.microsoft.com'
		headers={'Content-Type':'application/json','Ocp-Apim-Subscription-Key': subscriptionKey,}
		params = urllib.urlencode({'visualFeatures': 'Categories,Description,Color','language': 'en',})
		body = {'url':imageUrl}
		repeats=scriptHandler.getLastScriptRepeatCount()
		ui.message(_("Fetching Image Description. Please wait."))
		response=self.getResponse(proxyIP,proxyPort,uri_base,params,body,headers)
		if response.status!=200:
			log.debugWarning("reason:%s %s",response.status,response.reason)
		else:
			log.debugWarning("response received")
			dataMap=self.extractDataFromResponse(response)
		textList=[]
		if repeats==0:
			text="Description : "+dataMap['description']+"\n"+"Confidence : "+dataMap['confidence'] + "%"
			if text:
				textList.append(text)
			ui.message(" ".join(textList))
		elif repeats==1:
			text="Description : "+dataMap['description']+"\n"+"Confidence : "+dataMap['confidence'] + "% \nDominant Foreground Colour :"+dataMap['fgColor']+"\nDominant Background Colour :"+dataMap['bgColor']
			if text:
				textList.append(text)
			# Translators: title for formatting information dialog.
			ui.browseableMessage(("\n".join(textList) ) , _("Image Description"))

    __gestures = {
        "kb:nvda+g": "getImageDescription",
    }
        