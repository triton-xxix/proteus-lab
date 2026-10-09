"""Build rowkeeper.html: template.html with PDF.js 3.11.174 (cdnjs) inlined, so it works offline.

usage: python3 build.py   (writes rowkeeper.html next to this file)
"""
import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CDN = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/"


def fetch(name):
    with urllib.request.urlopen(CDN + name, timeout=60) as r:
        return r.read().decode("utf-8").replace("</script", "<\\/script")


lib, worker = fetch("pdf.min.js"), fetch("pdf.worker.min.js")
html = open(os.path.join(HERE, "template.html")).read()
# The worker code loads as a plain script: PDF.js then runs on the main thread (globalThis.pdfjsWorker),
# which needs no Worker from a blob URL. A blob worker hung under file:// in headless Chrome on 9 Oct.
inline = ('<script>' + worker + '</script>\n<script>' + lib + '</script>')
html = html.replace("<script>/*PDFJS*/</script>", inline)
out = os.path.join(HERE, "rowkeeper.html")
open(out, "w").write(html)
print("wrote", out, len(html.encode()), "bytes")
