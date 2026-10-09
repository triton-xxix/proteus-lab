"""Make test.html: rowkeeper.html plus a self-driving test that loads a generated two-page PDF,
sets rows per repeat to 4, presses + five times, and writes the state into <pre id=result>.
Run it twice in headless Chrome on one profile: the second run must restore row 5, repeat 1."""
import base64
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def pdf():
    objs = ["<< /Type /Catalog /Pages 2 0 R >>",
            "<< /Type /Pages /Kids [3 0 R 5 0 R] /Count 2 >>"]
    for n, text in ((4, "Row 1: k2, p2 to end"), (6, "Row 2: p2, k2 to end")):
        objs.append("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents %d 0 R "
                    "/Resources << /Font << /F1 7 0 R >> >> >>" % n)
        s = "BT /F1 24 Tf 72 760 Td (%s) Tj ET" % text
        objs.append("<< /Length %d >>\nstream\n%s\nendstream" % (len(s), s))
    objs.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    out, offs = "%PDF-1.4\n", []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += "%d 0 obj\n%s\nendobj\n" % (i, o)
    x = len(out)
    out += "xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    out += "".join("%010d 00000 n \n" % o for o in offs)
    out += "trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, x)
    return out.encode()


TEST = """<script>
(async () => {
  const out = document.createElement('pre'); out.id = 'result'; document.body.appendChild(out);
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  try {
    const bytes = Uint8Array.from(atob('%s'), c => c.charCodeAt(0));
    const f = new File([bytes], 'test-pattern.pdf', {type: 'application/pdf'});
    const k = 'rowkeeper:test-pattern.pdf:' + f.size;
    const before = localStorage.getItem(k);
    const dt = new DataTransfer(); dt.items.add(f);
    const inp = document.getElementById('file'); inp.files = dt.files;
    inp.dispatchEvent(new Event('change'));
    for (let i = 0; i < 100 && document.querySelectorAll('#doc canvas').length < 2; i++) await sleep(100);
    await sleep(300);
    const restored = {row: document.getElementById('row').textContent, rep: document.getElementById('rep').textContent};
    if (!before) {
      const per = document.getElementById('per'); per.value = '4'; per.dispatchEvent(new Event('change'));
      for (let i = 0; i < 5; i++) document.getElementById('rowUp').click();
    }
    const c = document.querySelector('#doc canvas');
    const px = c ? c.getContext('2d').getImageData(0, 0, c.width, c.height).data : [];
    let ink = 0; for (let i = 0; i < px.length; i += 4) if (px[i] < 128) ink++;
    out.textContent = 'RESULT ' + JSON.stringify({hint: document.getElementById('hint').textContent, run: before ? 2 : 1, pages: document.querySelectorAll('#doc canvas').length,
      dark_pixels_page1: ink, restored, now: {row: document.getElementById('row').textContent,
      rep: document.getElementById('rep').textContent}, saved: JSON.parse(localStorage.getItem(k))});
  } catch (e) { out.textContent = 'RESULT ERR ' + e; }
})();
</script>
</body>"""

html = open(os.path.join(HERE, "rowkeeper.html")).read()
html = html.replace("</body>", TEST % base64.b64encode(pdf()).decode(), 1)
open(os.path.join(HERE, "test.html"), "w").write(html)
print("wrote test.html")
