# -*- coding: UTF-8 -*-
# Copyright (C) 2005-2012 J. David Ibáñez <jdavid.ibp@gmail.com>
# Copyright (C) 2006-2009 Hervé Cauwelier <herve@oursours.net>
# Copyright (C) 2007-2008 Henry Obein <henry.obein@gmail.com>
# Copyright (C) 2008 Gautier Hayoun <gautier.hayoun@supinfo.com>
# Copyright (C) 2008, 2010-2011 David Versmisse <versmisse@lil.univ-littoral.fr>
# Copyright (C) 2009 Sylvain Taverne <taverne.sylvain@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Import from the Standard Library
from json import dumps, loads
from datetime import timedelta
from time import strftime

# Import from itools
from itools.i18n import init_language_selector
from itools.log import Logger, register_logger, log_info
from context import select_language
from context import WebLogger, get_context, set_context
from soup import SoupServer, SoupMessage
from dispatcher import URIDispatcher

class WebServer(SoupServer):

    access_log = None
    event_log = None

    database = None
    session_timeout = timedelta(0)

    accept_cors = False
    dispatcher = URIDispatcher()

    request_time = 0  # Initialized after each request (in handle_request)


    def __init__(self, root, access_log=None, event_log=None):
        super(WebServer, self).__init__()
        # The application's root
        self.root = root
        # Access log
        logger = AccessLogger(access_log, rotate=timedelta(weeks=3))
        register_logger(logger, 'itools.web_access')
        # Events log
        logger = WebLogger(event_log)
        register_logger(logger, 'itools.web')
        # Useful the current uploads stats
        self.upload_stats = {}


    def log_access(self, host, request_line, status_code, body_length):
        if host:
            host = host.split(',', 1)[0].strip()
        now = strftime('%d/%b/%Y:%H:%M:%S %z')
        message = '%s - - [%s] "%s" %d %d %.3f\n' % (host, now, request_line,
                                                     status_code, body_length,
                                                     self.request_time)
        log_info(message, domain='itools.web_access')


    def listen(self, address, port):
        # Language negotiation
        init_language_selector(select_language)
        # Add handlers
        super(WebServer, self).listen(address, port)
        self.add_handler('*', self.star_callback)
        context = self.root.context_cls(
            database=self.database, server=self)
        self.add_handler('/', context.handle_request)
        # Say hello
        address = address if address is not None else '*'
        print 'Listen %s:%d' % (address, port)


    def do_request(self, method='GET', path='/', headers=None, body='',
            context=None, as_json=False, user=None):
        """Experimental method to do a request on the server"""
        headers = headers or {}
        # I'm not a robot
        headers['User-Agent'] = 'Firefox'
        # Build headers
        if body and not as_json:
            headers['content-type'] = 'application/x-www-form-urlencoded'
        elif body and as_json is True:
            body = dumps(body)
            headers['content-type'] = 'application/json'
        if as_json is True:
            headers['accept'] = 'application/json'
        # Build soup message
        message = SoupMessage()
        message.set_message(method, 'http://localhost' + path, body)
        for name, value in headers.items():
            message.set_request_header(name, value)
        # Get context
        context = context or get_context() or self.get_fake_context()
        context.server = self
        # Login user: XXX do not works
        if user:
            context.login(user)
            context.user = user
        # Do request
        context = context.handle_request(message, path)
        # Transform result
        if context.entity is None:
            response = None
        elif as_json:
            response = loads(context.entity)
        else:
            response = context.entity
        # Return result
        return {'status': context.status,
                'method': context.method,
                'entity': response,
                'context': context}


    def get_fake_context(self):
        context = self.root.context_cls()
        context.soup_message = SoupMessage()
        context.path = '/'
        context.database = self.database
        context.server = self
        set_context(context)
        return context


    def set_upload_stats(self, upload_id, uploaded_size, total_size):
        """This function is called by the C part of your server.
        """
        if uploaded_size is None or total_size is None:
            self.upload_stats.pop(upload_id, None)
        else:
            self.upload_stats[upload_id] = (uploaded_size, total_size)


    def stop(self):
        super(WebServer, self).stop()
        if self.access_log:
            self.access_log_file.close()


    def star_callback(self, soup_message, path):
        """This method is called for the special "*" request URI, which means
        the request concerns the server itself, and not any particular
        resource.

        Currently this feature is only supported for the OPTIONS request
        method:

          OPTIONS * HTTP/1.1
        """
        method = soup_message.get_method()
        if method != 'OPTIONS':
            soup_message.set_status(405)
            soup_message.set_header('Allow', 'OPTIONS')
            return

        # XXX Hardcoded
        known_methods = ['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE']
        soup_message.set_status(200)
        soup_message.set_header('Access-Control-Allow-Methods', ', '.join(known_methods))



class AccessLogger(Logger):

    def format(self, domain, level, message):
        return message
