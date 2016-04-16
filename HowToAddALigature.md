# How to add a new ligature, by example

Here is how we added the double-slash ligature.

First we need to create four glyphs for the ligature character: two for *italic* and two for *roman*; in each case one glyph will be thicker than the other. Here was my process:
 1. Open the font `Blackfont/RomanMasters/SourceCodePro_0.ufo/` in fontforge.
 2. Create a new font.
 3. Copy the slash from the SourceCodePro_0 font to the new font.
 4. Edit the glyph, in this case create a copy of the slash and move them around. Possibly edit the glyph's width.
 5. Right-click the glyph, choose `Glyph info`, and set the unicode for it to `-1` and the name to `slash_slash.`
 6. Go to `file -> generate fonts` and generate a *unified font object* font somewhere temporary.
 7. In the `glyphs` subdirectory there should be a file slash_slash.glif
 8. Copy this file into `Blackfont/RomanMasters/SourceCodePro_0.ufo/glyphs/`

 11. Repeat 1 to 8 for the fonts:
 ```
 Blackfont/RomanMasters/SourceCodePro_2.ufo/
 Blackfont/ItalicMasters/SourceCodePro-Italic_0.ufo/
 Blackfont/ItalicMasters/SourceCodePro-Italic_2.ufo/
 ```
 The number-2 fonts are the thicker ones.  I have no idea why the `_1` files don't need it.

---------------------

Finally, we need to run the script:
```
 python mlig.py +G slash_slash
```
which adds the glyph's name to a bunch of xml files (use `-G` to remove), and edit `ligatures.fea`. Append the line:
```
    sub slash slash by slash_slash;                         # //
```
(don't forget the `by`).

Then rebuild the font and voilá.

How to rebuild the font
===============================

You need to have python2-fonttools module installed, as well as Adobe Font Development Kit for OpenType.

If your default python system is Python 3, you might get various "Syntax Error" messages. Then remember to create a Python 2 virtual environment:
```
virtualenv -p /usr/bin/python2.7 --system-site-packages --no-setuptools --no-pip --no-wheel /tmp/temp-python2
```
Then to rebuild the font:
```
source /tmp/temp-python2/bin/activate
./buildInstances.sh
./build.sh
deactivate
```
