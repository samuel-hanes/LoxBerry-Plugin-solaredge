# LoxBerry-Plugin-solaredge
Brigde for Solaredge PV <-> Loxone Miniserver.

Designed to work on LoxBerry > v2.2

This Plugin gets every 5 minutes the actual power values and sends a calculated balance to the miniserver via udp messages. It is negative when power to the grid is injected and positive when power from the grid is consumed. The value is then ready to use with the loxone energy manager.

More information and documentation can be found at:
https://www.loxwiki.eu/display/LOXBERRY/Solaredge+Brigde

Known Issues:
* None
