#!/usr/bin/env python

#
# Generated  by generateDS.py.
# Python 2.7.13 (default, Jan 19 2017, 14:48:08)  [GCC 6.3.0 20170118]
#
# Command line options:
#   ('--no-dates', '')
#   ('--no-versions', '')
#   ('--disable-xml', '')
#   ('--disable-generatedssuper-lookup', '')
#   ('--member-specs', 'list')
#   ('-f', '')
#   ('-a', 'xsd:')
#   ('-o', 'tests/disable_xml_super2_sup.py')
#   ('-s', 'tests/disable_xml_super2_sub.py')
#   ('--super', 'disable_xml_super2_sup')
#   ('--no-warnings', '')
#
# Command line arguments:
#   tests/disable_xml_super.xsd
#
# Command line:
#   generateDS.py --no-dates --no-versions --disable-xml --disable-generatedssuper-lookup --member-specs="list" -f -a "xsd:" -o "tests/disable_xml_super2_sup.py" -s "tests/disable_xml_super2_sub.py" --super="disable_xml_super2_sup" --no-warnings tests/disable_xml_super.xsd
#
# Current working directory (os.getcwd()):
#   generateds
#

import sys
## from lxml import etree as etree_

import disable_xml_super2_sup as supermod

## def parsexml_(infile, parser=None, **kwargs):
##     if parser is None:
##         # Use the lxml ElementTree compatible parser so that, e.g.,
##         #   we ignore comments.
##         parser = etree_.ETCompatXMLParser()
##     doc = etree_.parse(infile, parser=parser, **kwargs)
##     return doc

#
# Globals
#

ExternalEncoding = 'ascii'

#
# Data representation classes
#


class PackageTypeSub(supermod.PackageType):
    def __init__(self, Address=None):
        super(PackageTypeSub, self).__init__(Address, )
supermod.PackageType.subclass = PackageTypeSub
# end class PackageTypeSub


