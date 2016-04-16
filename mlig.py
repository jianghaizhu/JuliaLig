#!/usr/bin/python
import argparse
import sys
import xml.etree.ElementTree as ET
import os
import io

TESTING = False

XML_PREAMBLE = '<?xml version="1.0" encoding="UTF-8"?>\n' + \
               '<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'


def addremove_glyph(font_dir, glyph, add=True):
    remove = not add
    filename = os.path.join(font_dir, 'glyphs/contents.plist')
    print("Processing file '%s'." % filename)
    if not os.path.isfile(filename):
        raise Exception("Bad format: no file '%s'." % filename)
    tree = ET.parse(filename)
    # encoding = tree.docinfo.encoding
    root = tree.getroot()

    dict_element = root.find('dict')

    found = False

    dict_children = dict_element.iter()
    for child in dict_children:
        if child.tag != 'key': continue
        key = child.text
        if glyph == key:
            if add:
                print("Warning: glyph '%s' already found in '%s'." % (glyph, filename))
            else:
                print("Removing glyph '%s' from '%s'." % (glyph, filename))
                sibling = next(dict_children)
                dict_element.remove(child)
                dict_element.remove(sibling)
            found = True

            break

    if add and not found or remove and found:
        if add:
            add_element(dict_element, 'key', glyph)
            add_element(dict_element, 'string', glyph + '.glif')
            add_indentation(dict_element)
        if TESTING:
            file = io.BytesIO()
        else:
            file = open(filename, 'wb')
        file.write(XML_PREAMBLE.encode('utf-8'))
        tree.write(file, 'utf-8')  # , encoding=encoding)
        if TESTING:
            print("Test output:")
            print(file.getvalue()[-1000:].decode("utf-8"))
        file.close()
    elif remove and not found:
        print("Warning: glyph '%s' not found in file '%s'." % (glyph, filename))

    filename = os.path.join(font_dir, 'lib.plist')
    print("Processing file '%s'." % filename)
    if not os.path.isfile(filename):
        raise Exception("Bad format: no file '%s'." % filename)
    tree = ET.parse(filename)
    # encoding = tree.docinfo.encoding
    root = tree.getroot()

    dict_element = root.find('dict')

    glyph_order_array = None
    dict_children = dict_element.iter()
    for child in dict_children:
        if child.tag == 'key' and child.text == 'public.glyphOrder':
            glyph_order_array = next(dict_children)
            break
    if glyph_order_array is None: raise Exception("Bad format in file '%s', 'public.glyphOrder' array not found.")

    found = False
    array_children = glyph_order_array.iter()
    for child in array_children:
        key = child.text
        if glyph == key:
            if add:
                print("Warning: glyph '%s' already found in '%s'." % (glyph, filename))
            else:
                print("Removing glyph '%s' from '%s'." % (glyph, filename))
                glyph_order_array.remove(child)
            found = True
            break

    if add and not found or remove and found:
        if add:
            add_element(glyph_order_array, 'string', glyph, indentation=8)
            add_indentation(dict_element, indentation=8)
        if TESTING:
            file = io.BytesIO()
        else:
            file = open(filename, 'wb')
        file.write(XML_PREAMBLE.encode('utf-8'))
        tree.write(file, 'utf-8')  # , encoding=encoding)
        if TESTING:
            print("Test output:")
            print(file.getvalue()[-1000:].decode("utf-8"))
        file.close()
    elif remove and not found:
        print("Warning: glyph '%s' not found in file '%s'." % (glyph, filename))


def add_indentation(parent, indentation=4):
    parent[-1].tail = "\n" + " " * indentation


def add_element(parent, tag, text, indentation=4):
    add_indentation(parent, indentation)
    e = ET.Element(tag)
    e.text = text
    parent.append(e)


def print_help():
    print(
"""
usage:
        mlig.py +G glyph [glyph ...]
            Adds glyphs to the various font masters.

        mlig.py -G glyph [glyph ...]
            Removes glyphs from the various font masters.

        mlig.py +L glyph glyph [glyph ...] ligature-glyph
            Adds a new ligature associated with the given ligature-glyph.

        mlig.py +L glyph glyph [glyph ...]
            Removes a ligature.

NOTE: All glyphs are defined by their character name, not by the characters themselves.
"""
    )


def abort(message=None):
    if message is not None: print(message)
    print_help()
    exit(-1)


def add_ligature(glyphs, ligature_glyph):
    raise NotImplementedError()


def remove_ligature(glyphs):
    raise NotImplementedError()


if __name__ == "__main__":

    font_dirs = [
        "RomanMasters/SourceCodePro_0.ufo/",
        "RomanMasters/SourceCodePro_2.ufo/",
        "ItalicMasters/SourceCodePro-Italic_0.ufo/",
        "ItalicMasters/SourceCodePro-Italic_2.ufo/"
    ]

    if len(sys.argv) < 2:
        abort()

    command = sys.argv[1]
    if command[1] == "G" and command[0] in ['+', '-']:
        add = command[0] == '+'
        if len(sys.argv) < 3: abort("Need to specify at least one glyph to %s." % ("add" if add else "remove"))
        glyphs = sys.argv[2:]
        for glyph in glyphs:
            for font_dir in font_dirs:
                addremove_glyph(font_dir, glyph, add=add)
    elif command == "+L":
        if len(sys.argv) < 5: abort("Need to specify at least two glyphs and one ligature-glyph.")
        glyphs = sys.argv[2:-1]
        ligature_glyph = sys.argv[-1]
        add_ligature(glyphs, ligature_glyph)
    elif command == "-L":
        if len(sys.argv) < 4: abort("Need to specify at least two glyphs to form a ligature.")
        glyphs = sys.argv[2:-1]
        ligature_glyph = sys.argv[-1]
        remove_ligature(glyphs)
    else:
        abort("Unknown command '%s'." % command)


