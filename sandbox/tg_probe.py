import sys,re,html,subprocess
for c in sys.argv[1:]:
    t=subprocess.run(['/usr/bin/curl','-s','-m','20','-A','proteus-lab/0.1 research','-L','https://t.me/s/'+c],capture_output=True,text=True).stdout
    msgs=re.findall(r'tgme_widget_message_text[^>]*>(.*?)</div>',t,re.S)
    dates=re.findall(r'datetime="([^"]+)"',t)
    txt=re.sub('<[^>]+>',' ',' '.join(msgs))
    addr=re.findall(r'\b[1-9A-HJ-NP-Za-km-z]{32,44}\b',txt)
    print(c,len(t),'msgs',len(msgs),'last',dates[-1:],'addr',len(addr),'|',html.unescape(txt[-120:]).replace('\n',' '))
