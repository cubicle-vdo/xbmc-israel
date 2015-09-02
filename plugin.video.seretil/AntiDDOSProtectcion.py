# -*- coding: utf-8 -*-
import urllib2,urlparse,re,cookielib,xbmc,xbmcaddon,os,time

def decryptCFDDOSProtection(url,agent='',DomainD='',AddonID=''):
	class NoRedirection(urllib2.HTTPErrorProcessor):    
		def http_response(self,request,response):
			return response
	
	user_dataDir = xbmc.translatePath(xbmcaddon.Addon(AddonID).getAddonInfo("profile")).decode("utf-8")
	if not os.path.exists(user_dataDir):
		os.makedirs(user_dataDir)
	
	url=url.replace('https://','http://')
	cf_html_file=os.path.join(user_dataDir,'CF_html.txt')
	if len(agent)==0: agent='Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'
	cj=cookielib.CookieJar()
	opener=urllib2.build_opener(NoRedirection, urllib2.HTTPCookieProcessor(cj))
	opener.addheaders=[('User-Agent', agent)]
	response=opener.open(url)
	try: cookie2=str(response.headers.get('Set-Cookie'))
	except: cookie2=''
	result=response.read()
	CF_SaveFile(cf_html_file,result)
	s='<link rel="shortcut icon" href="/Content/images/favicon.ico" type="image/x-icon" /><script type="text/javascript">'
	if s in result:
		result=result.split(s)[-1]
	jschl=re.compile('name="jschl_vc" value="(.+?)"/>').findall(result)[0]
	try: cfPass=re.compile('name="pass" value="(.+?)"/>').findall(result)[0]
	except: cfPass=''
	try: cfFormAction=re.compile('<form id="challenge-form" action="(/[^"]+)" method="\D+">').findall(result)[0]
	except: cfFormAction='/cdn-cgi/l/chk_jschl'
	init=re.compile('setTimeout\(function\(\){\s*\n*\s*(?:var \D,\D,\D,\D, [0-9A-Za-z]+={"[0-9A-Za-z]+"|.*?.*):(.*?)};').findall(result)[-1]
	builder=re.compile(r"challenge-form\'\);\s*\n*\r*\a*\s*(.*)a.v").findall(result)[0]
	try: TimeToWait=int(re.compile(r"f.submit\(\);\s*\n*\s*},\s*(\d+)\)").findall(result)[-1])
	except: TimeToWait=9000
	decryptVal=CF_parseJSString(init)
	lines=builder.split(';')
	for line in lines:
		if len(line)>0 and '=' in line:
			try:
				sections=line.split('=')
				line_leftside=sections[0]
				line_val=CF_parseJSString(sections[1])
				decryptVal=int(eval(str(decryptVal)+sections[0][-1]+str(line_val)))
			except: pass
			
	DomainFix=urlparse.urlparse(url).netloc
	if '/' in DomainFix: DomainFix=DomainFix.split('/')[0]
	if 'www.' in DomainFix: DomainFix=DomainFix.replace('www.','')
	answer=decryptVal+len(DomainFix)
	try: Domain=re.compile('(\D+://.+?)/').findall(url)[0]
	except: Domain=DomainD
	if cfPass=='':
		query='%s%s?jschl_vc=%s&jschl_answer=%s'%(str(Domain),str(cfFormAction),str(jschl),str(answer))
	else:
		query='%s%s?jschl_vc=%s&pass=%s&jschl_answer=%s'%(str(Domain),str(cfFormAction),str(jschl),str(cfPass),str(answer))
	xbmc.sleep(TimeToWait)
	opener=urllib2.build_opener(NoRedirection,urllib2.HTTPCookieProcessor(cj))
	opener.addheaders=[('User-Agent',agent)]
	response=opener.open(query)
	cookie=str(response.headers.get('Set-Cookie'))
	result=response.read()
	response.close()
	cf_html_file=os.path.join(user_dataDir,'CF_htmlr.txt')
	CF_SaveFile(cf_html_file,result)
	xbmc.sleep(2000)
	FoundCookies=''
	if (len(str(cookie )) > 5): FoundCookies+='\r\nSet-Cookie3: '+str(cookie)+'\r\n'
	p=[]
	p.append(['cf_clearance=','cf_clearance="'])
	p.append(['; ','"; '])
	p.append([' expires=',' expires="'])
	p.append([' path=',' path="'])
	p.append([' domain=',' domain="'])
	p.append(['',''])
	for p1,p2 in p:
		FoundCookies=FoundCookies.replace(p1,p2)

	return FoundCookies

def CF_parseJSString(s):
    try:
        offset=1 if s[0]=='+' else 0
        return int(eval(s.replace('!+[]','1').replace('!![]','1').replace('[]','0').replace('(','str(')[offset:]))
    except:
        return
		
def CF_SaveFile(path,data):
	try:
		file=open(path,'w')
		file.write(data)
		file.close()
	except: pass
	
def CF_OpenFile(path,d=''):
	try:
		if os.path.isfile(path): ## File found.
			file=open(path,'r')
			contents=file.read()
			file.close()
			return contents
		else: return d ## File not found.
	except: return d
