# Výtvarná reference Alzáka

`alzak_sprite_concept.png` a `alzak_sprite_pistol_reference.png` jsou koncepční
obrázky vytvořené vestavěným ImageGenem podle uživatelem dodané vizuální
reference. `alzak_sprite_runtime_atlas.png` je bezztrátová archivní kopie
transparentního runtime atlasu.

Použitý prompt požadoval originálního přátelského zeleného mimozemského maskota
pro 2D plošinovku ve čtyřech pózách (idle, run, air, hurt), s limetkově zelenou
postavou, stříbrnou tunikou a botami, bez textu, log, značek a dalších postav.
Druhá reference stanovuje boční pohled, osm animačních póz a kompaktní
laserovou pistoli bez loga. Hra načítá jejich finální stylizovanou high-poly
podobu z `assets/images/alzak_atlas.png`; obdélníky jednotlivých póz jsou
uvedeny v manifestu a kreslí se v rozlišení 150 × 190 px. Generátor atlas
nepřepisuje, pouze jej indexuje a ověřuje jeho checksum.

Tři runtime pozadí `assets/images/bg_*.png` jsou přímo autorské výstupy
ImageGenu ve stylizovaném high-poly 3D vzhledu. Manifest je označuje
`generated: false`; generátor je nepřepisuje, pouze ověří a znovu zapíše jejich
checksumy do manifestu.
