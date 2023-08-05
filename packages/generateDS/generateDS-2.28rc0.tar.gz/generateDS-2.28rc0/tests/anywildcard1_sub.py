#!/usr/bin/env python

#
# Generated  by generateDS.py.
# Python 2.7.13 (default, Jan 19 2017, 14:48:08)  [GCC 6.3.0 20170118]
#
# Command line options:
#   ('--no-dates', '')
#   ('--no-versions', '')
#   ('--silence', '')
#   ('--member-specs', 'list')
#   ('-f', '')
#   ('-o', 'tests/anywildcard2_sup.py')
#   ('-s', 'tests/anywildcard2_sub.py')
#   ('--super', 'anywildcard2_sup')
#
# Command line arguments:
#   tests/anywildcard.xsd
#
# Command line:
#   generateDS.py --no-dates --no-versions --silence --member-specs="list" -f -o "tests/anywildcard2_sup.py" -s "tests/anywildcard2_sub.py" --super="anywildcard2_sup" tests/anywildcard.xsd
#
# Current working directory (os.getcwd()):
#   generateds
#

import sys
from lxml import etree as etree_

import anywildcard2_sup as supermod

def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        parser = etree_.ETCompatXMLParser()
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

#
# Globals
#

ExternalEncoding = 'ascii'

#
# Data representation classes
#


class PlantType_singleSub(supermod.PlantType_single):
    def __init__(self, name=None, anytypeobjs_=None, description=None):
        super(PlantType_singleSub, self).__init__(name, anytypeobjs_, description, )
supermod.PlantType_single.subclass = PlantType_singleSub
# end class PlantType_singleSub


class PlantType_multipleSub(supermod.PlantType_multiple):
    def __init__(self, name=None, anytypeobjs_=None, description=None):
        super(PlantType_multipleSub, self).__init__(name, anytypeobjs_, description, )
supermod.PlantType_multiple.subclass = PlantType_multipleSub
# end class PlantType_multipleSub


class DescriptionTypeSub(supermod.DescriptionType):
    def __init__(self, name=None, size=None):
        super(DescriptionTypeSub, self).__init__(name, size, )
supermod.DescriptionType.subclass = DescriptionTypeSub
# end class DescriptionTypeSub


class CatalogTypeSub(supermod.CatalogType):
    def __init__(self, name=None, catagory=None):
        super(CatalogTypeSub, self).__init__(name, catagory, )
supermod.CatalogType.subclass = CatalogTypeSub
# end class CatalogTypeSub


class PlantType_single_nochildSub(supermod.PlantType_single_nochild):
    def __init__(self, anytypeobjs_=None):
        super(PlantType_single_nochildSub, self).__init__(anytypeobjs_, )
supermod.PlantType_single_nochild.subclass = PlantType_single_nochildSub
# end class PlantType_single_nochildSub


class PlantType_multiple_nochildSub(supermod.PlantType_multiple_nochild):
    def __init__(self, anytypeobjs_=None):
        super(PlantType_multiple_nochildSub, self).__init__(anytypeobjs_, )
supermod.PlantType_multiple_nochild.subclass = PlantType_multiple_nochildSub
# end class PlantType_multiple_nochildSub


def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    rootClass = supermod.GDSClassesMapping.get(tag)
    if rootClass is None and hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'PlantType_single'
        rootClass = supermod.PlantType_single
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
##     if not silence:
##         sys.stdout.write('<?xml version="1.0" ?>\n')
##         rootObj.export(
##             sys.stdout, 0, name_=rootTag,
##             namespacedef_='',
##             pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'PlantType_single'
        rootClass = supermod.PlantType_single
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    mapping = {}
    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
##     if not silence:
##         content = etree_.tostring(
##             rootElement, pretty_print=True,
##             xml_declaration=True, encoding="utf-8")
##         sys.stdout.write(content)
##         sys.stdout.write('\n')
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False):
    from StringIO import StringIO
    parser = None
    doc = parsexml_(StringIO(inString), parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'PlantType_single'
        rootClass = supermod.PlantType_single
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
##     if not silence:
##         sys.stdout.write('<?xml version="1.0" ?>\n')
##         rootObj.export(
##             sys.stdout, 0, name_=rootTag,
##             namespacedef_='')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'PlantType_single'
        rootClass = supermod.PlantType_single
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
##     if not silence:
##         sys.stdout.write('#from anywildcard2_sup import *\n\n')
##         sys.stdout.write('import anywildcard2_sup as model_\n\n')
##         sys.stdout.write('rootObj = model_.rootClass(\n')
##         rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
##         sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()
