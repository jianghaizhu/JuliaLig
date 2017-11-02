# How to add a new ligature

Here is how we added the double-slash ligature.

First you need to build the font on your machine.

How to build the font
==============================

You need to have Python 2.7+, with the [fonttools](https://github.com/fonttools/fonttools) module installed, as well as [Adobe Font Development Kit](https://github.com/adobe-type-tools/afdko) for OpenType.

The command
```
./buildInstances.sh
```

Will take the thin and fat fonts, and interpolate them to get the various thicknesses.

The command
```
./build.sh
```
Will add the ligature table.

After both commands are run, the fonts are in the `target` folder.


If you have Python 3
===========================

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
An example for ligature
==============================

Then you need to create four glyphs for the ligature character: two for *italic* and two for *roman*; in each case one glyph will be thicker than the other. Here was my process:
 1. Open the font `JuliaLig/target/JuliaLig-Regular.otf` in [FontForge](https://fontforge.github.io/en-US/).
 2. Create a new font.
 3. Copy the slash to the new font.
 4. Edit the glyph, in this case create a copy of the slash and move them around. Possibly edit the glyph's width.
 5. Right-click the glyph, choose `Glyph info`, and set the unicode for it to `-1` and the name to `slash_slash.`
 6. Go to `file -> generate fonts` and generate a **unified font object** font somewhere temporary.
 7. In the `glyphs` subdirectory there should be a file slash_slash.glif
 8. Copy this file into `JuliaLig/RomanMasters/SourceCodePro_0.ufo/glyphs/`

 11. Repeat 1 to 8 for the fonts:
 ```
 JuliaLig/RomanMasters/SourceCodePro_2.ufo/
 JuliaLig/ItalicMasters/SourceCodePro-Italic_0.ufo/
 JuliaLig/ItalicMasters/SourceCodePro-Italic_2.ufo/
 ```
The font for *italic* is `JualiaLig/target/JuliaLig-It.otf`. The number-2 fonts are the thicker ones. You can use `JuliaLig/target/JuliaLig-Bold.otf` and `JuliaLig/target/JuliaLig-BoldIt.otf`.  I have no idea why the `_1` files don't need it.

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
