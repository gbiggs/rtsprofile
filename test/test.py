# -*- Python -*-
# -*- coding: utf-8 -*-

'''rtsprofile

Copyright (C) 2009-2010
    Geoffrey Biggs
    RT-Synthesis Research Group
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt

File: test.py

Unit tests.

'''

__version__ = '$Revision: $'
# $Source$


from rtsprofile.rts_profile import RtsProfile
import sys


def main(argv):
    test_file_name = argv[1]

    rtsprofile = RtsProfile(xml_spec_file=test_file_name)
    print rtsprofile

    if len(argv) > 2:
        rtsprofile.save_to_xml_file(argv[2])


if __name__ == '__main__':
    sys.exit(main(sys.argv))


# vim: tw=79

