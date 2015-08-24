# -*- coding: utf-8 -*-
import urllib, re, json
import common, urlresolver

def ResolveUrl(url):
	link = False
	try:
		result=common.OPEN_URL(url)
		matches=re.compile('<div id="embed_code".+?<iframe.+?src=["|\'](.*?)["|\'].+?<\/iframe><\/div>',re.I+re.M+re.U+re.S).findall(result)
		url = matches[0]
		if "filehoot" in url:
			url = url.replace("/embed-","/")
			url = "{0}.html".format(url[:url.rfind('-')])
			html = common.OPEN_URL(url)
			id = re.compile("http://filehoot.com/(.+?).html", re.I+re.M+re.U+re.S).findall(url)
			user_data = {'op':'download1','usr_login':'','id':id[0],'fname':'','referer':'','method_free':'Continue+to+watch+your+Video'}
			html = common.OPEN_URL(url, user_data=user_data)
			matches = re.compile('{file:["|\'](.+?)["|\']', re.I+re.M+re.U+re.S).findall(html)
			if len(matches) > 0:
				link = matches[0]
		elif "allmyvideos" in url:
			html = common.OPEN_URL(url)
			#print html
			matches = re.compile('["|\']file["|\'].+?:.+?["|\'](.+?)["|\']',re.I+re.M+re.U+re.S).findall(html)
			if len(matches) > 0:
				link = matches[0]
		elif "goodvideohost" in url:
			url = url.replace("/embed-","/")
			html = common.OPEN_URL(url)

			url = re.compile('method="POST" action=\'(.+?)\'', re.I+re.M+re.U+re.S).findall(html)[0]
			op =  re.compile('name="op" value="(.+?)"', re.I+re.M+re.U+re.S).findall(html)[0]
			usr_login =  re.compile('name="usr_login" value="(.+?)"', re.I+re.M+re.U+re.S).findall(html)[0]
			id = re.compile('name="id" value="(.+?)"', re.I+re.M+re.U+re.S).findall(html)[0]
			fname =  re.compile('name="fname" value="(.+?)"', re.I+re.M+re.U+re.S).findall(html)[0]
			referer =  re.compile('name="referer" value="(.+?)"', re.I+re.M+re.U+re.S).findall(html)[0]
			hash = re.compile('name="hash" value="(.+?)"', re.I+re.M+re.U+re.S).findall(html)[0]
			imhuman =  re.compile('name="imhuman" value="(.+?)"', re.I+re.M+re.U+re.S).findall(html)[0]
			
			#user_data = {'op':'download1','usr_login':'','id':id[0],'fname':'','referer':'','hash':hash[0],'imhuman':'Proceed+to+video'}
			user_data = {'op':urllib.quote_plus(op),'usr_login':urllib.quote_plus(usr_login),'id':urllib.quote_plus(id),'fname':urllib.quote_plus(fname),'referer':urllib.quote_plus(referer),'hash':urllib.quote_plus(hash),'imhuman':urllib.quote_plus(imhuman)}
			html = common.OPEN_URL(url, user_data=user_data)

			matches = re.compile('{file:"(.+?)"', re.I+re.M+re.U+re.S).findall(html)
			if len(matches) > 0:
				link = matches[0]	
		else:
			if "movreel" in url:
				url = url.replace("/embed-","/")
			item = urlresolver.HostedMediaFile(url)
			link = urlresolver.resolve(item.get_url())
	except:
			pass
	return link
	
def GetYifyLinks(url):
	sources = []
	try:
		result=common.OPEN_URL(url)
		matches=re.compile('<div id="embed_code".+?<iframe.+?src=["|\'](.*?)["|\'].+?<\/iframe><\/div>',re.I+re.M+re.U+re.S).findall(result)
		url = matches[0]
		html = common.OPEN_URL(url)
		links = re.compile('pic=([^&]+)').findall(html)
		for i in links:
			try:
				user_data = {'url': i, 'fv': '16'}
				html = common.OPEN_URL("http://yify.tv/player/pk/pk/plugins/player_p2.php", user_data=user_data)
				result = json.loads(html)
				try: sources.append({'quality': '1080p', 'url': [i['url'] for i in result if i['width'] == 1920 and 'google' in i['url']][0]})
				except: pass
				try: sources.append({'quality': '720p', 'url': [i['url'] for i in result if i['width'] == 1280 and 'google' in i['url']][0]})
				except: pass

				try: sources.append({'quality': '1080p', 'url': [i['url'] for i in result if i['width'] == 1920 and not 'google' in i['url'] and not 'mediafire' in i['url']][0]})
				except: pass
				try: sources.append({'quality': '720p', 'url': [i['url'] for i in result if i['width'] == 1280 and not 'google' in i['url'] and not 'mediafire' in i['url']][0]})
				except: pass
			except:
				pass
	except:
		pass
	return sources