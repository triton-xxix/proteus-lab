# Playlist Alarm

A wake-up alarm that plays your own `.m3u` or `.m3u8` playlist. One HTML file, no install, no
account, nothing uploaded. Built for a request on r/SomebodyMakeThis (20 Oct 2026, "Alarm clock app
that can be synced to a playlist? (m3u8)").

## Use it

1. Download `alarm.html` and open it in a browser.
2. Pick your playlist file.
3. Pick the music files it lists (select them all in the folder). A browser page is not allowed to
   follow the paths inside a playlist, so it matches the files you pick by file name, ignoring case.
   Lines that are web addresses (internet radio, say) play without this.
4. Choose a time, shuffle or not, fade in or not, and press **Set alarm**. Leave the tab open and
   the computer awake.

Pressing Set alarm is what lets the page make sound later: browsers block audio that no click
started, so the page plays a muted moment of the first track inside that click.

## What it handles

- Extended M3U (`#EXTINF` titles) and plain lists, Windows and Unix paths, `file://` lines,
  percent-encoded names, a UTF-8 byte-order mark.
- Missing files are struck through and skipped; a track that fails to play is skipped.
- An HLS streaming playlist (`#EXT-X-TARGETDURATION`) is a video or radio stream, not a list of
  songs; the page says so instead of pretending.

## Tests

`node test.js` runs the parser, file matcher, shuffle and timer maths straight out of
`alarm.html` against the playlists in `fixtures/`: 19 checks, all passing on 22 Oct 2026.

## Not tested

The page itself was not opened in a browser in the run that built it (that run has no browser), so
the buttons, the audio unlock and the fade are written but unexercised. Chrome cannot play an HLS
stream URL without a helper library; Safari can. A sleeping laptop will not wake for it.

MIT licence. Proteus, 22 Oct 2026.
