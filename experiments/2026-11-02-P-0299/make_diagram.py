"""P-0299: fill stack-diagram's template with the Proteus nightly stack, as an agent following SKILL.md would."""
import re

SKILL = "/Users/triton/PROTEUS/sandbox/stack-diagram/stack-diagram-main/skills/stack-diagram"
OUT = "/Users/triton/PROTEUS/experiments/2026-11-02-P-0299/proteus-nightly.html"

t = open(SKILL + "/assets/template.html", encoding="utf-8").read()

head = '''<header class="head">
    <div>
      <div class="kicker">proteus / nightly / 2026-11</div>
      <h1>The nightly run</h1>
    </div>
    <p class="lede">A scheduler starts the run, Python desks pull and paper-trade, git commits the proof to GitHub, Pages shows it.</p>
  </header>'''
t = re.sub(r'<header class="head">.*?</header>', head, t, count=1, flags=re.S)

canvas = '''<div class="canvas">
    <div class="group ga" style="left:212px; top:60px; width:340px; height:210px;">
      <div class="g-label"><img src="%%ICON_python%%" alt="">Desks</div>
    </div>
    <div class="group gb" style="left:600px; top:60px; width:340px; height:210px;">
      <div class="g-label"><img class="lt" src="%%ICON_github%%" alt=""><img class="dk" src="%%ICON_github_dark%%" alt="">GitHub</div>
    </div>
    <svg class="edges" viewBox="0 0 1000 540" aria-hidden="true">
      <defs>
        <marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse">
          <path d="M0 0 L10 5 L0 10 z" fill="context-stroke"/>
        </marker>
      </defs>
      <path class="e" d="M148 150 H266" marker-end="url(#ar)"/>
      <text class="el a" x="207" y="142" text-anchor="middle">23:15</text>
      <path class="e" d="M336 150 H426" marker-end="url(#ar)"/>
      <path class="e" d="M496 150 H656" marker-end="url(#ar)"/>
      <text class="el a" x="576" y="142" text-anchor="middle">git push</text>
      <path class="e" d="M726 150 H816" marker-end="url(#ar)"/>
    </svg>
    <div class="node" style="left:46px;top:120px">
      <div class="tile"><img src="%%ICON_pythonanywhere%%" alt=""></div>
      <div class="name"><span>Scheduler</span></div><div class="role"><span>nightly task</span></div>
    </div>
    <div class="node" style="left:236px;top:120px">
      <div class="tile"><img src="%%ICON_python%%" alt=""></div>
      <div class="name"><span>Python</span></div><div class="role"><span>desk scripts</span></div>
    </div>
    <div class="node" style="left:396px;top:120px">
      <div class="tile"><img src="%%ICON_store%%" alt=""></div>
      <div class="name"><span>Ledgers</span></div><div class="role"><span>csv and jsonl</span></div>
    </div>
    <div class="node" style="left:626px;top:120px">
      <div class="tile"><img src="%%ICON_github%%" alt=""></div>
      <div class="name"><span>proteus-lab</span></div><div class="role"><span>repo</span></div>
    </div>
    <div class="node" style="left:786px;top:120px">
      <div class="tile"><img src="%%ICON_page%%" alt=""></div>
      <div class="name"><span>GitHub Pages</span></div><div class="role"><span>lab page</span></div>
    </div>
  </div>'''
t = re.sub(r'<div class="canvas">.*?\n  </div>\n  </div>', canvas + "\n  </div>", t, count=1, flags=re.S)
t = t.replace("<!-- FOOT-LEFT: author / one-liner -->", "Proteus, P-0299")
t = re.sub(r"<!-- FOOT-RIGHT:.*?-->", "icons: svgl / Lucide", t, flags=re.S)
open(OUT, "w", encoding="utf-8").write(t)
print("wrote", OUT, len(t), "chars; ICON tokens", len(re.findall(r"%%ICON_\w+%%", t)))
