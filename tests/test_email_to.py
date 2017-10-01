#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `email_to` package."""

import pytest


import email_to


@pytest.fixture
def message():
    """ Simple message """
    msg = email_to.Message('# A Test Message', style='h1 { color: blue }')
    msg.add('This message is only a test of the alert system')
    return msg


def test_build_message(message):
    """ Test that a message can be created and added to directly """
    msg = message

    msg_string = str(msg)
    assert '# A Test Message' in msg_string
    assert 'This message is only a test of the alert system' in msg_string

    msg_html = msg.html
    assert '<html>' in msg_html
    assert '<head></head>' in msg_html
    assert '<body>' in msg_html
    assert 'style="color:blue">' in msg_html
    assert 'A Test Message' in msg_html
    assert '<p>This message is only a test of the alert system' in msg_html


def test_empty_message():
    """ Test that a message passed an empty body gets created """
    msg = email_to.Message()
    msg_string = str(msg)
    assert msg_string == ''

    msg_html = msg.html
    assert msg.html == ''


def test_message_mime(message):
    """ Test that a message can form a valid MIMEMultiPart object """
    mime = message.mime()
    mime_string = str(mime)
    assert 'Content-Type' in mime_string
    assert 'multipart/alternative' in mime_string
    #assert 'From' in mime_string
    assert 'MIME-Version:' in mime_string
    assert 'Content-Type: text/plain; charset="us-ascii"' in mime_string
    assert '# A Test Message' in mime_string
    assert 'Content-Type: text/html; charset="us-ascii"' in mime_string
    assert '<h1 style="color:blue">A Test Message</h1>' in mime_string
