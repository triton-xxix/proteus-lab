import sys,re,subprocess,html
for u in sys.argv[1:]:
    t=subprocess.run(['/usr/bin/curl','-s','-m','20','-A','proteus-lab/0.1 research','-L',u],capture_output=True,text=True).stdout
    items=re.findall(r'<item[ >].*?</item>|<entry[ >].*?</entry>',t,re.S)
    dates=re.findall(r'<(?:pubDate|published|updated)>([^<]+)<',t)
    titles=re.findall(r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>',t,re.S)
    print(u,len(t),'items',len(items),'newest',dates[:1],'oldest',dates[-1:])
    print('   ',html.unescape(titles[1] if len(titles)>1 else '')[:120])
