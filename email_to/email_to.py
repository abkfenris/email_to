# -*- coding: utf-8 -*-

"""Main module."""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import markdown
import premailer


class Message(object):
    """ A simple email message made of Markdown strings

    A Message is a simplified version of a MIMEMultipart email message.
    Instead of having to seperately construct HTML and text version of
    an email, you can build a Message by adding lines of Markdown formatted
    strings.

    """
    def __init__(self, body=None, style=None, server=None):
        """
        Args:
            body (str, bytes, iterable of strings): The body of the email.
                It does not need to be complete, as you can add to it later.
            style (str): CSS formatting to be applied to HTML formatted verion
                of email.
            server (EmailServer): An EmailServer instance allowing a message
                to be sent directly from it's `send` method.

        """
        if body is None:
            self.body = []
        else:
            if any((isinstance(body, str), isinstance(body, bytes))):
                body = [body]
            self.body = body
        self.style = style
        self.server = server

    def add(self, line):
        """ Adds a new Markdown formatted line to the current email body """
        self.body.append(line)

    @property
    def html(self):
        """ Returns HTML formatted and styled version of body """
        html = markdown.markdown('\n'.join(self.body))
        if self.style:
            return premailer.transform('<style>\n' + self.style +
                                       '\n</style>\n' + html)
        return html

    def __str__(self):
        return '\n'.join(self.body)

    def __repr__(self):
        return '<Message: {0} and {1} more lines>'.format(
                self.body[0], (len(self.body) - 1))

    def mime(self):
        """ Returns a MIMEMultipart message """
        msg = MIMEMultipart('alternative')

        msg.attach(MIMEText(str(self), 'plain'))
        msg.attach(MIMEText(self.html, 'html'))

        return msg

    def send(self, to, subject):
        """ Sends the formatted message to given recripient

        args:
            to (:obj:str, iterable of :obj:`str`): Email addresses to send to
            subject (str): Subject line of email to send

        """
        self.server.send_message(self, to, subject)


class EmailServer(object):
    def __init__(self, url, port, email, password):
        self.url = url
        self.port = port
        self.email_address = email
        self.password = password

    def _login(self):
        self.server = smtplib.SMTP(self.url, self.port)
        self.server.starttls()
        self.server.login(self.email_address, self.password)

    def _logout(self):
        self.server.quit()

    def quick_email(self, to, subject, body, style=None):
        message = Message(body, style=style)

        self.send_message(message, to, subject)

    def send_message(self, message, to, subject):
        message = message.mime()

        message['From'] = self.email_address
        message['To'] = to

        message['Subject'] = subject

        self._login()
        self.server.sendmail(self.email_address, to, message.as_string())
        self._logout()

    def message(self, body=None, style=None):
        return Message(body=body, style=style, server=self)
