# $Id$

import xmlrpclib, pycurl, cStringIO

class CURLTransport(xmlrpclib.Transport):
    """Handles a cURL HTTP transaction to an XML-RPC server."""

    xmlrpc_h = [ "User-Agent: PycURL XML-RPC", "Content-Type: text/xml" ]

    def __init__(self, username=None, password=None):
        self.c = pycurl.init()
        self.c.setopt(pycurl.POST, 1)
        self.c.setopt(pycurl.HTTPHEADER, self.xmlrpc_h)
        if username != None and password != None:
            self.c.setopt(pycurl.USERPWD, '%s:%s' % (username, password))

    def request(self, host, handler, request_body, verbose=0):
        b = cStringIO.StringIO()
        self.c.setopt(pycurl.URL, 'http://%s%s' % (host, handler))
        self.c.setopt(pycurl.POSTFIELDS, request_body)
        self.c.setopt(pycurl.WRITEFUNCTION, b.write)
        self.c.setopt(pycurl.VERBOSE, verbose)
        self.verbose = verbose
        try:
            self.c.perform()
        except pycurl.error, v:
            raise xmlrpclib.ProtocolError(
                host + handler,
                v[0], v[1], None
                )
        b.seek(0)
        return self.parse_response(b)


if __name__ == "__main__":
    ## Test
    server = xmlrpclib.ServerProxy("http://betty.userland.com",
                                   transport=CURLTransport())
    print server

    try:
        print server.examples.getStateName(41)
    except xmlrpclib.Error, v:
        print "ERROR", v