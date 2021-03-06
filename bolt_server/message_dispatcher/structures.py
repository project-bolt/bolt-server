'''
File: structures.py
Description: Message dispatcher related structures
Date: 29/09/2017
Author: Saurabh Badhwar <sbadhwar@redhat.com>
'''
import hashlib
import json

class Message(object):
    """Structure for handling new message types.

    Provides general functionality for all the messages to go through
    and pass there structural representation for validation.

    The message structure looks like:
    message = {
        message_name: [message_strcuture]
    }
    """

    def __init__(self):
        """Initialize the Message Structure"""

        self.messages = {}
        self.message_count = 0
        self.error_count = 0

    def add_message(self, message_name, message_structure):
        """Add a new message to the message structure

        Keyword arguments:
        message_name -- The name of the message
        message_strcuture -- The strcuture the message follows

        Raises:
            RuntimeError if message_name already exists
        """

        if message_name in self.messages.keys():
            raise RuntimeError("The specified message already exists")

        self.messages[message_name] = message_structure

    def get_message(self, message_name):
        """Get the message structure associated with the name

        Keyword arguments:
        message_name -- The name of the message whose structure is requested

        Raises:
            KeyError when the message is not found

        Returns:
            Mixed The message structure
        """

        if message_name not in self.messages.keys():
            raise KeyError("The requested message structure was not found")

        return self.messages[message_name]

    def get_message_list(self):
        """Get all the registered messages

        Return:
            List of registered messages
        """

        return self.messages.keys()

    def remove_message(self, message_name):
        """Remove the message from the registered list

        Keyword arguments:
        message_name -- The name of the message to be removed
        """

        if message_name in self.messages.keys():
            del self.messages[message_name]

class MessagePacket(object):
    """The message pakcet Structure for the Bolt Server

    Encapsulates the message along with a unique recognizable id so as to manage
    the message lifecycle

    Message Packet: {
        identifier: <unique_identifier>,
        message: Message
    }
    """

    def __init__(self, message):
        """Initialize the Message Packet"""

        self.message_packet = {}
        self.message_digest = hashlib.sha256(str(message)).hexdigest()
        self.message_packet['id'] = self.message_digest
        self.message_packet['payload'] = message

    def get_packet(self):
        """Get the JSON formatted packet which can be transmitted

        Returns: JSON
        """

        return (self.message_digest, json.dumps(self.message_packet))

class MessageQueue(object):
    """We use a message queue to track the responses received for the message

    Message Queue keeps a track of unique message identifiers along with the
    response they they generate so as to decide what to do next
    """

    def __init__(self):
        """Initialize the message queue"""

        self.message_queue = {}

    def queue(self, message_identifier):
        """Queue a newly sent message

        Keyword arguments:
        message_identifier -- The unique identifier pertaining to message
        """

        self.message_queue[message_identifier] = 'Awaited'

    def update_status(self, message_identifier, status):
        """Update the status of a sent message

        Keyword arguments:
        message_identifier -- The identifier to update
        status -- The new status of the message

        Raises:
            KeyError if the message is not present in the queue
        """

        if message_identifier not in self.message_queue.keys():
            raise KeyError("Cannot update status for an inexistant message")

        self.message_queue[message_identifier] = status
