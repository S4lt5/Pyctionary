from twisted.internet.protocol import ClientFactory
from twisted.internet.task import deferLater, cooperate
from zope.interface import implementer

__author__ = 'matthewgalligan'
import time,Queue
from twisted.internet import reactor, protocol, endpoints
from twisted.protocols import basic
from doodle import Doodle
from threading import Thread
import threading



def chunkyWorkload(reactor, protocol):
    while True:
        if not Communicator.doodle_queue.empty():
            while not Communicator.doodle_queue.empty():
                line = Communicator.doodle_queue.get()
                protocol.sendLine(line)
        yield deferLater(reactor, 0.2, lambda: None)

#largely cribbed from docs at https://twistedmatrix.com/trac/
class PubProtocol(basic.LineReceiver):
    def __init__(self, factory):
        self.factory = factory



    def connectionMade(self):
        self.factory.clients.add(self)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)

    def lineReceived(self, line):
        try:
            doodle = Doodle.parse(line)
            self.communicator.draw_callback(doodle,retransmit=False)
        except:
            raise ValueError("Got an invalid doodle. Ignoring")


class PubClientProtocol(basic.LineReceiver):



    #blank the canvas on new player
    def connectionMade(self):
        print("Connected protocol")
        self.queue = Queue.Queue()
        #self.transport.registerProducer(QueueProducer(self.transport), False)
        self.sendLine("3,0,0")
        gen = chunkyWorkload(self.transport.reactor, self)
        self.task = cooperate(gen)


    def lineReceived(self, line):
        try:
            print("got a line")
            doodle = Doodle.parse(line)
            self.communicator.draw_callback(doodle,retransmit=False)
            #for c in self.factory.clients:
            #   c.sendLine("Got it")


        #    c.sendLine("<{}> {}".format(self.transport.getHost(), line))
        except:
            raise ValueError("Got an invalid doodle. Ignoring")

class PubFactory(protocol.Factory):
    def __init__(self):
        self.clients = set()

    def send_line(self,line):
        for c in self.clients:
            print("Sending line")
            #print("Sending line to " + c.__str__())
            c.sendLine(line)


    def buildProtocol(self, addr):
        #build the protocol, and return the callback draw function that is available on this reactor
        return PubProtocol(self)


class PubClientFactory(ClientFactory):
    def startedConnecting(self, connector):
        print 'Started to connect.'

    def send_line(self,line):
        if self.protocol is not None:
            print("Sending line " + line)
            self.protocol.transport.write(line + "\r\n")
            self.protocol.sendLine(line)

    def buildProtocol(self, addr):
        print 'Connected.'
        self.protocol = PubClientProtocol()

        return self.protocol

    def clientConnectionLost(self, connector, reason):
        print 'Lost connection.  Reason:', reason

    def clientConnectionFailed(self, connector, reason):
        print 'Connection failed. Reason:', reason


class Communicator(object):
    doodle_queue = Queue.Queue()
    '''
    A communicator object provides networking ability for the pyctionary client.

    If not connected to any other client, handles this situation gracefully

    finally, provides connectivity status (this probably isn't going to work super great!)
    '''
    def __init__(self,host=True,remote_address=None,draw_callback=None):
        '''
        Initialize the communicator. Default options are: Host, with no remote outbound connection attempt
        :param host: if true, the communicator will listen for external connections
        :param remote_address:  if host is false, remote_address must contain an IP/dns name of a remote host
        :param draw_callback: if present, this callback will happen each time a new doodle is received
        :return: nothing
        '''
        self.hosting = host
        self.remote_addresss = remote_address
        self.connection = None
        self.draw_callback = draw_callback
        self.network_thread = None
        self.send_callback = None
        #queue of outbound

        PubProtocol.communicator = self


    def connect(self,host = None,remote_address=None):
        '''
        Connect with the settings defined on init, unless overriding values are specified explicitly
        :param host: If present, assigns a new hosting value
        :param remote_address: If present, assigns a new remote address value
        :return: nothing
        '''

        if host is not None:
            self.hosting = host

        if remote_address is not None:
            self.remote_addresss = remote_address

        #close any connection that may exist
        self.disconnect()

        #this is a cop-out but probably way beyond the scope of this project!
        if self.network_thread is not None:
            print("Network thread is already active, aborting. Please restart application if you are having problems.")
            return

        if self.hosting:
            print("Listening!")
            #this can be called to send text over the twisted channel

            factory = PubFactory()
            self.send_callback = factory.send_line
            endpoints.serverFromString(reactor, "tcp:4444").listen(factory)
            #set threads to daemon so they don't keep app alive
            self.network_thread = Thread(target=reactor.run, args=(False,))
            self.network_thread.setDaemon(True)
            self.network_thread.start()
        else:
            print("Connecting to " + self.remote_addresss)
            factory = PubClientFactory()
            self.send_callback = factory.send_line
            reactor.connectTCP(self.remote_addresss, 4444, factory)

            self.network_thread = Thread(target=reactor.run, args=(False,))
            self.network_thread.setDaemon(True)
            self.network_thread.start()




    def disconnect(self):
        '''
        Disconnect, if connected or a connection object exists
        :return: nothing
        '''
        print("This doesn't realy work. Try closing the app and re-connecting if necessary.")




    def transmit_doodle(self,doodle):
        '''
        Transmit a doodle to be rendered remotely
        :param doodle: (GUI.Doodle) the graph piece to draw
        :return: nothing
        '''
        if self.send_callback is not None:
            Communicator.doodle_queue.put(doodle.__str__())
            #self.send_callback(doodle.__str__())