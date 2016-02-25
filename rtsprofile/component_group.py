# -*- Python -*-
# -*- coding: utf-8 -*-

'''rtsprofile

Copyright (C) 2009-2015
    Geoffrey Biggs
    RT-Synthesis Research Group
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the GNU Lesser General Public License version 3.
http://www.gnu.org/licenses/lgpl-3.0.en.html

File: component_group.py

Object representing a component group.

'''

__version__ = '$Revision: $'
# $Source$


from rtsprofile import RTS_NS, RTS_NS_S
from rtsprofile.utils import validate_attribute, string_types


##############################################################################
## ComponentGroup object

class ComponentGroup(object):
    '''A group of components in the RT system.'''

    def __init__(self, group_id='', members=[]):
        '''Constructor.

        @param group_id ID of the group.
        @type group_id str
        @param members Members of the group. At least one must be present.
        @type members list

        '''
        validate_attribute(group_id, 'component_group.groupID',
                           expected_type=string_types(), required=False)
        self._group_id = group_id
        validate_attribute(members, 'component_group.Members',
                           expected_type=list, required=False)
        self._members = members

    def __str__(self):
        result = 'Group ID: {0}\n'.format(self.group_id)
        if self.members:
            result += 'Members:\n'
            for m in self.members:
                result += '  {0}\n'.format(m)
        return result[:-1] # Lop off the last new line

    @property
    def group_id(self):
        '''The ID used to distinguish this group in the RT system.

        Example:
        >>> g = ComponentGroup()
        >>> g.group_id = "test"

        Invalid assignment should throw exception:
        >>> g.group_id = 1
        Traceback (most recent call last):
        ...
        InvalidTypeError: ('component_group.groupID', <type 'int'>, [<type 'str'>, <type 'unicode'>])
        '''
        return self._group_id

    @group_id.setter
    def group_id(self, group_id):
        validate_attribute(group_id, 'component_group.groupID',
                           expected_type=string_types(), required=True)
        self._group_id = group_id

    @property
    def members(self):
        '''A list of the components in the group.

        At least one must be present.

        Example:
        >>> import rtsprofile.component
        >>> g = ComponentGroup()
        >>> g.members = [rtsprofile.component.Component()]

        Invalid assignment should throw exception:
        >>> g.members = []
        Traceback (most recent call last):
        ...
        RequiredAttributeError: component_group.Members
        >>> g.members = 1
        Traceback (most recent call last):
        ...
        InvalidTypeError: ('component_group.Members', <type 'int'>, <type 'list'>)
        '''
        return self._members

    @members.setter
    def members(self, members):
        validate_attribute(members, 'component_group.Members',
                           expected_type=list, required=True)
        self._members = members

    def parse_xml_node(self, node):
        '''Parse an xml.dom Node object representing a component group into
        this object.

        '''
        self.group_id = node.getAttributeNS(RTS_NS, 'groupId')
        self._members = []
        for c in node.getElementsByTagNameNS(RTS_NS, 'Members'):
            self._members.append(TargetComponent().parse_xml_node(c))
        return self

    def parse_yaml(self, node):
        '''Parse a YAML specification of a component group into this
        object.

        '''
        self.group_id = y['groupId']
        self._members = []
        if 'members' in y:
            for m in y.get('members'):
                self._members.append(TargetComponent().parse_yaml(m))
        return self

    def save_xml(self, doc, element):
        '''Save this component group into an xml.dom.Element object.'''
        element.setAttributeNS(RTS_NS, RTS_NS_S + 'groupID', self.group_id)
        for m in self.members:
            new_element = doc.createElementNS(RTS_NS, RTS_NS_S + 'Members')
            m.save_xml(doc, new_element)
            element.appendChild(new_element)

    def to_dict(self):
        '''Save this component group to a dictionary.'''
        d = {'groupId': self.group_id}
        members = []
        for m in self.members:
            members.append(m.to_dict())
        if members:
            d['members'] = members
        return d



# vim: tw=79

