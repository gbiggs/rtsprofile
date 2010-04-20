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

File: message_sending.py

Objects for the message sending interface.

'''

__version__ = '$Revision: $'
# $Source$


from rtsprofile import RTS_NS, RTS_NS_S, RTS_EXT_NS, RTS_EXT_NS_S
from rtsprofile.targets import TargetExecutionContext
from rtsprofile.utils import get_direct_child_elements_xml, \
                             indent_string, validate_attribute


##############################################################################
## MessageSending base object

class MessageSending(object):
    '''Defines the orderings and conditions components in the RT system for
    various actions.

    '''

    def __init__(self, targets=[]):
        '''@param targets Orderings and conditions.'''
        validate_attribute(targets, 'message_sending.Targets',
                           expected_type=list, required=False)
        self._targets = targets

    def __str__(self):
        result = self.__class__.__name__ + '\n'
        if self.targets:
            result += 'Targets:\n'
            for t in self.targets:
                result += '{0}\n'.format(indent_string(str(t)))
        return result[:-1] # Lop off the last new line

    @property
    def targets(self):
        '''Orderings and conditions.'''
        return self._targets

    @targets.setter
    def targets(self, targets):
        validate_attribute(targets, 'message_sending.Targets',
                           expected_type=list, required=False)
        self._targets = targets

    def parse_xml_node(self, node):
        '''Parse an xml.dom Node object representing a message sending object
        into this object.

        '''
        self._targets = []
        for c in node.getElementsByTagNameNS(RTS_NS, 'Targets'):
            if c.getAttributeNS(RTS_NS, 'waitTime'):
                new_target = WaitTime()
            elif c.getAttributeNS(RTS_NS, 'timeout') or \
                    c.getAttributeNS(RTS_NS, 'sendingTiming') or \
                    c.getElementsByTagNameNS(RTS_NS, 'PrecedingComponents'):
                new_target = Preceding()
            else:
                new_target = Condition()
            new_target.parse_xml_node(c)
            self._targets.append(new_target)
        return self

    def save_xml(self, doc, element):
        '''Save this message_sending object into an xml.dom.Element object.'''
        for cond in self._targets:
            new_element = doc.createElementNS(RTS_NS, RTS_NS_S + 'Targets')
            cond.save_xml(doc, new_element)
            element.appendChild(new_element)


##############################################################################
## StartUp object

class StartUp(MessageSending):
    '''Specifies the start order and conditions of components when the RT
    system is started.

    '''
    pass


##############################################################################
## ShutDown object

class ShutDown(MessageSending):
    '''Specifies the stop order and conditions of components when the RT system
    is stopped.

    '''
    pass


##############################################################################
## Activation object

class Activation(MessageSending):
    '''Specifies the activation order and conditions of components when the RT
    system is activated.

    '''
    pass


##############################################################################
## Deactivation object

class Deactivation(MessageSending):
    '''Specifies the deactivation order and conditions of components when the RT
    system is deactivated.

    '''
    pass


##############################################################################
## Resetting object

class Resetting(MessageSending):
    '''Specifies the reset order and conditions of components when the RT
    system is reset.

    '''
    pass


##############################################################################
## Initialize object

class Initialize(MessageSending):
    '''Specifies the initialisation order and conditions of components when the
    RT system is initialised.

    '''
    pass


##############################################################################
## Finalize object

class Finalize(MessageSending):
    '''Specifies the finalisation order and conditions of components when the
    RT system is finalised.

    '''
    pass


##############################################################################
## Condition base object

class Condition(object):
    '''Specifies execution orderings and conditions for RT components in the RT
    system.

    Execution conditions can include the time to wait before executing and
    order of precedence for components. The involved RT component is specified
    using @ref TargetExecutionContext.

    '''

    def __init__(self, sequence=0, target_component=TargetExecutionContext()):
        '''Constructor.

        @param sequence Execution order of the target component.
        @type sequence int
        @param target_component The target of the condition.
        @type target_component TargetComponent
        '''
        validate_attribute(sequence, 'conditions.sequence',
                           expected_type=int, required=False)
        self._sequence = sequence
        validate_attribute(target_component, 'conditions.TargetComponent',
                           expected_type=TargetExecutionContext,
                           required=True)
        self._target_component = target_component
        self._properties = {}

    def __str__(self):
        result = 'Sequence: {0}\nTargetEC:\n{1}\n'.format(self.sequence,
                indent_string(str(self.target_component)))
        if self.properties:
            result += 'Properties:\n'
            for p in self.properties:
                result += '  {0}: {1}\n'.format(p, self.properties[p])
        return result[:-1] # Lop off the last new line

    @property
    def sequence(self):
        '''The execution order of the target components for the various
        actions.

        '''
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        validate_attribute(sequence, 'conditions.sequence',
                           expected_type=int, required=False)
        self._sequence = sequence

    @property
    def target_component(self):
        '''Target component of the condition.'''
        return self._target_component

    @target_component.setter
    def target_component(self, target_component):
        validate_attribute(target_component, 'conditions.TargetComponent',
                           expected_type=TargetExecutionContext,
                           required=True)
        self._target_component = target_component

    @property
    def properties(self):
        '''Miscellaneous properties.

        Stores key/value pair properties.

        Part of the extended profile.

        '''
        return self._properties

    @properties.setter
    def properties(self, properties):
        validate_attribute(properties, 'conditions.ext.Properties',
                           expected_type=dict, required=False)
        self._properties = properties

    def parse_xml_node(self, node):
        '''Parse an xml.dom Node object representing a condition into this
        object.

        '''
        self.sequence = int(node.getAttributeNS(RTS_NS, 'sequence'))
        c = node.getElementsByTagNameNS(RTS_NS, 'TargetComponent')
        if c.length != 1:
            raise InvalidParticipantNodeError
        self.target_component = TargetExecutionContext().parse_xml_node(c[0])
        for c in get_direct_child_elements_xml(node, prefix=RTS_EXT_NS,
                                               local_name='Properties'):
            name, value = parse_properties_xml(c)
            self._properties[name] = value
        return self

    def save_xml(self, doc, element):
        '''Save this condition into an xml.dom.Element object.'''
        element.setAttributeNS(RTS_NS, RTS_NS_S + 'sequence',
                               str(self.sequence))
        new_element = doc.createElementNS(RTS_NS, RTS_NS_S + 'TargetComponent')
        self.target_component.save_xml(doc, new_element)
        element.appendChild(new_element)
        for p in self.properties:
            new_prop_element = doc.createElementNS(RTS_EXT_NS,
                                                   RTS_EXT_NS_S + 'Properties')
            properties_to_xml(new_prop_element, p, self.properties[p])
            element.appendChild(new_prop_element)


##############################################################################
## Preceding object

class Preceding(Condition):
    '''Specifies that the target RT component should precede other RT
    components that are part of the same action (e.g. activation) when that
    action is executed.

    '''

    def __init__(self, sequence=0, target_component=TargetExecutionContext(),
                 timeout=0, sending_timing='', preceding_components=[]):
        '''Constructor.

        @param sequence Execution order of the target component.
        @type sequence int
        @param target_component The target of the condition.
        @type target_component TargetComponent
        @param timeout Status check timeout.
        @type timeout int
        @param sending_timing Timing for executing actions.
        @type sending_timing str
        @param preceding_components Preceding components of the condition.
        @type preceding components list(TargetExecutionContext)

        '''
        super(Preceding, self).__init__(sequence, target_component)
        validate_attribute(timeout, 'preceding.timeout',
                           expected_type=int, required=False)
        self._timeout = timeout
        validate_attribute(sending_timing, 'preceding.sendingTiming',
                           expected_type=[str, unicode], required=False)
        self._sending_timing = sending_timing
        validate_attribute(preceding_components,
                           'preceding.PrecedingComponents',
                           expected_type=list, required=False)
        self._preceding_components = preceding_components

    def __str__(self):
        result = 'Timeout: {0}\nSending timing: {1}\n{2}'.format(self.timeout,
                self.sending_timing, Condition.__str__(self))
        if self.preceding_components:
            for pc in self.preceding_components:
                result += '\nPreceding component:\n{0}'.format(\
                        indent_string(str(pc)))
        return result

    @property
    def timeout(self):
        '''Time out for checking if the target component has executed the
        action successfully.

        Can be zero. Specified in milliseconds.

        '''
        return self._timeout

    @timeout.setter
    def timeout(self, timeout):
        validate_attribute(timeout, 'preceding.timeout',
                           expected_type=int, required=False)
        self._timeout = timeout

    @property
    def sending_timing(self):
        '''Timing for executing actions.

        Either wait for the preceding RT component to finish executing the
        action, or execute the action without waiting for the preceding RT
        component to finish. When not specified, the first option will be
        assumed.

        '''
        return self._sending_timing

    @sending_timing.setter
    def sending_timing(self, sending_timing):
        validate_attribute(sending_timing, 'preceding.sendingTiming',
                           expected_type=[str, unicode], required=False)
        self._sending_timing = sending_timing

    @property
    def preceding_components(self):
        '''Preceding components of this condition.'''
        return self._preceding_components

    @preceding_components.setter
    def preceding_components(self, preceding_components):
        validate_attribute(sending_timing, 'preceding.PrecedingComponents',
                           expected_type=list, required=False)
        self._preceding_components = preceding_components

    def parse_xml_node(self, node):
        '''Parse an xml.dom Node object representing a preceding condition into
        this object.

        '''
        super(Preceding, self).parse_xml_node(node)
        if node.hasAttributeNS(RTS_NS, 'timeout'):
            self.timeout = int(node.getAttributeNS(RTS_NS, 'timeout'))
        else:
            self.timeout = ''
        if node.hasAttributeNS(RTS_NS, 'sendingTiming'):
            self.sending_timing = node.getAttributeNS(RTS_NS, 'sendingTiming')
        else:
            self.sending_timing = ''
        for c in node.getElementsByTagNameNS(RTS_NS, 'PrecedingComponents'):
            self._preceding_components.append(TargetExecutionContext().parse_xml_node(c))
        return self

    def save_xml(self, doc, element):
        '''Save this preceding condition into an xml.dom.Element object.'''
        super(Preceding, self).save_xml(doc, element)
        if self.timeout:
            element.setAttributeNS(RTS_NS, RTS_NS_S + 'timeout', self.timeout)
        if self.sending_timing:
            element.setAttributeNS(RTS_NS, RTS_NS_S + 'sendingTiming',
                                   self.sending_timing)
        for pc in self._preceding_components:
            new_element = doc.createElementNS(RTS_NS,
                                              RTS_NS_S + 'PrecedingComponents')
            pc.save_xml(doc, new_element)
            element.appendChild(new_element)


##############################################################################
## WaitTime object

class WaitTime(Condition):
    '''Specifies the time to wait before executing the specified action on the
    target RT component. After the action command is received by the RT
    component, it will wait the specified length of time before executing it.

    '''

    def __init__(self, wait_time, sequence=0,
                 target_component=TargetExecutionContext()):
        '''Constructor.

        @param sequence Execution order of the target component.
        @type sequence int
        @param target_component The target of the condition.
        @type target_component TargetComponent
        @param wait_time The length of time to wait, in milliseconds.
        @type wait_time int

        '''
        super(WaitTime, self).__init__(sequence, target_component)
        validate_attribute(wait_time, 'wait_time.waitTime',
                           expected_type=int, required=False)
        self._wait_time = wait_time

    def __str__(self):
        return 'Wait time: {0}\n{1}'.format(self.wait_time,
                                            Condition.__str__(self))

    @property
    def wait_time(self):
        '''The length of time to wait before executing the specified action.

        In milliseconds.

        '''
        return self._wait_time

    @wait_time.setter
    def wait_time(self, wait_time):
        validate_attribute(wait_time, 'wait_time.waitTime',
                           expected_type=int, required=False)
        self._wait_time = wait_time

    def parse_xml_node(self, node):
        '''Parse an xml.dom Node object representing a wait_time condition into
        this object.

        '''
        Condition.parse_xml_node(self, node)
        self.wait_time = int(node.getAttributeNS(RTS_NS, 'waitTime'))
        return self

    def save_xml(self, doc, element):
        '''Save this wait_time condition into an xml.dom.Element object.'''
        super(WaitTime, self).save_xml(doc, element)
        element.setAttributeNS(RTS_NS, RTS_NS_S + 'waitTime', self.wait_time)


# vim: tw=79

