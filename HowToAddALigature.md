For example, here is how we added the double-slash ligature.

First we need to create four glyphs for the ligature character: two for *italic* and two for *roman*; in each case one glyph will be thicker than the other. Here was my process:
 1. Open the font `Hasklig/RomanMasters/SourceCodePro_0.ufo/` in fontforge.
 2. Create a new font.
 3. Copy the slash from the SourceCodePro_0 font to the new font.
 4. Edit the glyph, in this case create a copy of the slash and move them around. Possibly edit the glyph's width.
 5. Right-click the glyph, choose `Glyph info`, and set the unicode for it to `-1` and the name to `slash_slash.`
 6. Go to `file -> generate fonts` and generate a *unified font object* font somewhere temporary.
 7. In the `glyphs` subdirectory there should be a file slash_slash.glif
 8. Copy this file into `Hasklig/RomanMasters/SourceCodePro_0.ufo/glyphs/`
 9. Edit the XML file `Hasklig/RomanMasters/SourceCodePro_0.ufo/glyphs/contents.plist`, at the end of the `<dict>` element, add the two elements:
 ```
 <key>slash_slash</key>
 <string>slash_slash.glif</string>
 ```
 10. Edit the XML file `Hasklig/RomanMasters/SourceCodePro_0.ufo/lib.plist`, at the end of the `<dict>` element, add the two elements:
 ```
 <string>slash_slash</string>
 ```
 11. Repeat 1 to 10 for the fonts:
 ```
 Hasklig/RomanMasters/SourceCodePro_2.ufo/
 Hasklig/RomanMasters/SourceCodePro-Italic_0.ufo/
 Hasklig/RomanMasters/SourceCodePro-Italic_2.ufo/
 ```
 I have no idea why the `_1` files don't need it.

---------------------

Finally, we need to edit `ligatures.fea`. Append the line:
```
    sub slash slash by slash_slash;                         # //
```

Then rebuild the font and voilá.
