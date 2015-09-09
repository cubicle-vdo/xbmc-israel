# -*- coding: utf-8 -*-
import urllib, re, json
import common, urlresolver, jsunpack, xbmc, base64

def ResolveUrl(url):
	link = False
	try:
		result=common.OPEN_URL(url)
		matches=re.compile('<div id="embed_code".+?<iframe.+?src=["|\'](.*?)["|\'].+?<\/iframe><\/div>',re.I+re.M+re.U+re.S).findall(result)
		url = matches[0]
		print "Link URL: " + url 
		if "divxpress" in url:
			html = common.OPEN_URL(url)
			matches = re.compile('input type="hidden" name="(.*?)" value="(.*?)"', re.I+re.M+re.U+re.S).findall(html)
			user_data = {}
			for match in matches:
				user_data[match[0]] = match[1]
			html = common.OPEN_URL(url, user_data=user_data)
			matches = re.compile("<div id=\"player_code\"><script type='text/javascript'>(.*?)</script></div>", re.I+re.M+re.U+re.S).findall(html)
			unpack = jsunpack.unpack(matches[0])
			matches = re.compile('"src"value="(.*?)"', re.I+re.M+re.U+re.S).findall(unpack)
			link = "{0}|User-Agent={1}&Referer={2}".format(matches[0], common.GetUA(), url)
		else:
			if "movreel" in url:
				url = url.replace("/embed-","/")
			#elif "openload" in url:
			#	url = url.replace(".co",".io")
			item = urlresolver.HostedMediaFile(url)
			link = urlresolver.resolve(item.get_url())
	except Exception, e: 
		print e
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
	
def GetAdFlyLink(url):
	retUrl = None
	try:
		html = common.OPEN_URL(url)
		ysmm = re.findall(r"var ysmm =.*\;?", html)

		if len(ysmm) > 0:
			ysmm = re.sub(r'var ysmm \= \'|\'\;', '', ysmm[0])

			left = ''
			right = ''

			for c in [ysmm[i:i+2] for i in range(0, len(ysmm), 2)]:
				left += c[0]
				right = c[1] + right

			retUrl = base64.b64decode(left.encode() + right.encode())[2:].decode()

			if re.search(r'go\.php\?u\=', retUrl):
				retUrl = base64.b64decode(re.sub(r'(.*?)u=', '', retUrl)).decode()

	except Exception as e:
		print str(e)
		
	return retUrl