# Copyright 2009 Jason Stitt
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#----------------------------------------------------------------------------#
#
# PURPOSE: Create an easy way to have a single application made with Pylons
# and Routes handle URLs on multiple domain names (i.e. without splitting
# it into an application per domain.)
#
# REQUIREMENTS: Pylons (0.9.7) and Routes (1.11)
#
#----------------------------------------------------------------------------#

from pylons import config, url

def absolute_url(route_name, **kargs):
    """ Generate a qualified url using the Routes url() method, but using the
    'host' property of the selected route instead of the current hostname,
    if possible. 
    
    Recommended usage: import this function into your 'helpers.py'
    """
    
    kargs['qualified'] = True
    route = config['routes.map']._routenames.get(route_name)
    if route:
        host = route._kargs.get('host')
        if host:
            kargs['host'] = host
        protocol = route._kargs.get('protocol')
        if protocol:
            kargs['protocol'] = protocol
    return url(route_name, **kargs)
        
class HostCondition(object):
    """ Condition that restricts a Routes route to a given hostname or aliases.
    
    Usage example with submapper (in 'routing.py', with an existing map object):

    example_host = HostCondition('example.com')
    example_host.alias('localhost:5000')
    with map.submapper(**example_host.args) as submap:
        submap.connect("fubar", '/foo/bar', controller='foo', action='index')
        
    Usage example without submapper:
    
    example_host = HostCondition('example.com')
    map.connect('fubar', '/foo/bar', controller='foo', action='index',
        conditions=dict(function=example_host.test),
        host=example_host.canonical_hostname)
    """
    
    def __init__(self, canonical_hostname):
        self.canonical_hostname = canonical_hostname
        self.aliases = {canonical_hostname:1}

    def alias(self, hostname):
        """ Add an alternate hostname that satisfies this condition. """
        self.aliases[hostname] = 1

    def test(self, environ, match_dict):
        """ The function to use inside a 'conditions' dictionary when 
        creating a route. """
        host = environ.get('HTTP_HOST', '')
        return host in self.aliases

    @property
    def args(self):
        """ A dictionary containing 'host' and 'conditions' arguments to be
        passed in when creating a route. """
        return dict(
            host=self.canonical_hostname,
            conditions=dict(function=self.test))

