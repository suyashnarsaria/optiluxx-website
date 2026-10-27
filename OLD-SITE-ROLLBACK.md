# Old website: how to go back

Recorded 27 Oct 2026, before optiluxx.in was pointed to Netlify.

## DNS before the switch (at Interpole / up99plus nameservers)
| Record | Value before switch |
|---|---|
| optiluxx.in A | 144.76.104.62 |
| www.optiluxx.in CNAME | optiluxx.in |
| mail.optiluxx.in A | 144.76.104.62 (unchanged, email) |
| ftp.optiluxx.in A | 144.76.104.62 (unchanged) |
| MX | 10 mail.optiluxx.in (unchanged) |
| SPF | v=spf1 a mx ip4:144.76.104.62 include:spf.up99plus.com ~all (unchanged) |

To restore the old site: ask Interpole to set the optiluxx.in A record back to 144.76.104.62
and the www CNAME back to optiluxx.in. The old files stay on the Interpole hosting.

## Old site contents (static HTML, 25 pages, 106 files, ~9.6 MB)
index.html, pages/about.html, advOfOptiluxx.html, basics.html, lang.html, tips.html, bulb.html,
downlight.html, surface.html, tube.html, strip.html, premium.html, flood.html, dcrcob.html,
dcrtrack.html, dcrzoom.html, client.html, policy.html, career.html, support.html, cc.html,
catalogue.html (with Optiluxx-Catalogue.pdf), cont.html; folders css/, js/, imgs/, images/.
