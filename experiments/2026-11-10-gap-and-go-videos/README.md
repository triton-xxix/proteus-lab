# Five win-rate videos, checked for evidence (watched-it, 10 Nov 2026)

Question: tonight's edge ladder had Gap and go climb three weeks. What do YouTube's gap-and-go
videos claim, and do the numbers hold against the ladder?

What I ran: `pull.py`. One YouTube search ("gap and go strategy backtest win rate"), titles by
oEmbed, captions by youtube_transcript_api, first five ids with captions of 34 found. One id had
transcripts disabled. Raw captions are in `sandbox/watched-gapgo/` (gitignored); `videos.json` holds
word counts and the lines that carry a number next to a claim word.

What came back: not what I asked for. None of the five is a gap-and-go video. Four are Shorts of 18 to
60 seconds (55 to 168 words); one is a 23-minute walkthrough of a fair-value-gap model (the word "gap"
68 times, all in that sense).

| video | length | number lines | what is claimed |
|---|---|---|---|
| DodgysDD, "Only The Top 2% Use This ICT Strategy" | 24 s | 1 | "80% win rate", no trades |
| Chart Fanatics, "98% WIN RATE Strategy Revealed" | 60 s | 0 | 98% in the title only |
| Trade with Pat, "ORB Trading Strategy that ACTUALLY WINS" | 30 s | 0 | wins, no number |
| The Backtest Log, "Long vs Short ... Nasdaq" | 18 s | 0 | nothing in the captions |
| ReeseTradesNQ, "90% Win Rate IFVG Model" | 22.7 min | 2 | "90% win rate over the entire year", no count |

Against the ladder (`edges/scan/2026-11-10/LADDER.md`): nine plain ORB rules on 12 US stocks, all
negative in W1, W2 and W3. ORB 15m fade: 24.5% winners in W1 and +7.20%. So win rate alone does not
sort a winner from a loser in my own data.

Limits: one search, first five with captions, not the best five. The number-line filter is a regex
(a claim word and a digit in one caption line), so a number spoken across two lines, or shown on
screen and never said, is missed. I read captions and watched nothing. The gap-and-go claim itself is
still unchecked; a better query is a job for another Tuesday.
