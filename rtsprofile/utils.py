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

File: utils.py

Utility functions.

'''

__version__ = '$Revision: $'
# $Source$


import new
import re

from rtsprofile import RTS_EXT_NS, RTS_EXT_NS_S
from rtsprofile.exceptions import InvalidTypeError, RequiredAttributeError


###############################################################################
## Public API functions

def get_direct_child_elements_xml(node, prefix=None, local_name=None):
    for c in node.childNodes:
        matches = False
        if prefix:
            if c.prefix == prefix:
                matches = True
        if local_name:
            if c.localName == local_name:
                matches = True
            else:
                matches = False
        if matches:
            yield c


def indent_string(string, num_spaces=2):
    '''Add indentation to a string.

    Replaces all new lines in the string with a new line followed by the
    specified number of spaces, and adds the specified number of spaces to the
    start of the string.

    '''
    indent = ' '.ljust(num_spaces)
    return indent + re.sub('\n', '\n' + indent, string)


def parse_properties_xml(node):
    name = node.getAttributeNS(RTS_EXT_NS, 'name')
    value = node.getAttributeNS(RTS_EXT_NS, 'value')
    if not value:
        return name, None
    else:
        return name, value


def properties_to_xml(element, name, value=None):
    element.setAttributeNS(RTS_EXT_NS, RTS_EXT_NS_S + 'name', name)
    if value:
        element.setAttributeNS(RTS_EXT_NS, RTS_EXT_NS_S + 'value', value)


def validate_attribute(attr, name, expected_type=None, required=False):
    '''Validates that an attribute meets expectations.

    This function will check if the given attribute value matches a necessary
    type and/or is not None, an empty string, an empty list, etc. It will raise
    suitable exceptions on validation failure.

    @param attr The value to validate.
    @param name The attribute name to use in exceptions.
    @param expected_type The type the value must be. If None, no check is
    performed. If a list, attr must match one type in the list.
    @param required If the value must not be empty, e.g. not an empty string.
    @raises InvalidTypeError
    @raises RequiredAttributeError

    '''
    if expected_type:
        if type(expected_type) == list:
            if not _check_type(attr, expected_type):
                raise InvalidTypeError(name, type(attr), expected_type)
        else:
            if not _check_type(attr, [expected_type]):
                raise InvalidTypeError(name, type(attr), expected_type)
    if required and not attr:
        raise RequiredAttributeError(name)


##############################################################################
## Private functions

def _check_type(value, expected_types):
    # Check if the type of value is one of those listed in expected_types
    for et in expected_types:
        if type(et) == type and type(value) == et:
            return True
        elif type(et) == new.classobj and \
                value.__class__.__name__ == et.__name__:
            return True
    return False


# vim: tw=79

