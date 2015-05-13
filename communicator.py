__author__ = 'matthewgalligan'

class Communicator(object):
    '''
    A communicator object provides networking ability for the pyctionary client.

    If not connected to any other client, handles this situation gracefully

    finally, provides connectivity status (this probably isn't going to work super great!)
    '''
    def __init__(self,host=True,remote_address=None):
        '''
        Initialize the communicator. Default options are: Host, with no remote outbound connection attempt
        :param host: if true, the communicator will listen for external connections
        :param remote_address:  if host is false, remote_address must contain an IP/dns name of a remote host
        :return: nothing
        '''
        self.hosting = host
        self.remote_addresss = remote_address
        self.connection = None

    def connect(self,host = None,remote_address=None):
        '''
        Connect with the settings defined on init, unless overriding values are specified explicitly
        :param host: If present, assigns a new hosting value
        :param remote_address: If present, assigns a new remote address value
        :return: nothing
        '''

        if host is not None:
            self.host = host

        if remote_address is not None:
            self.remote_addresss = remote_address

        #close any connection that may exist
        if self.connection is not None:
            self.disconnect()


        if self.hosting:
            print("Listening!")
        else:
            print("Connecting to " + self.remote_addresss)


    def disconnect(self):
        if self.connection is not None:
            print("Disconnecting.")
        else:
            print("Nothing to disconnect from.")
