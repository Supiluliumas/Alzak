# Výtvarná reference Alzáka

`alzak_sprite_concept.png` je jednorázový koncepční obrázek vytvořený vestavěným
ImageGenem podle uživatelem dodané vizuální reference. Není načítán hrou a není
součástí deterministicky generovaných runtime assetů.

Použitý prompt požadoval originálního přátelského zeleného mimozemského maskota
pro 2D plošinovku ve čtyřech pózách (idle, run, air, hurt), s limetkově zelenou
postavou, stříbrnou tunikou a botami, bez textu, log, značek a dalších postav.
Runtime sprity v `assets/images/player_*.png` tento koncept zjednodušují na
čitelnou podobu 64 × 96 px a generuje je deterministicky
`tools/generate_placeholders.py`.
