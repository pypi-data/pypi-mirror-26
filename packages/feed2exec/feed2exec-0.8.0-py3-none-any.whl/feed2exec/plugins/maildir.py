from __future__ import division, absolute_import
from __future__ import print_function


import logging
import mailbox
import os.path

from feed2exec.email import make_message
import feed2exec.utils as utils


class output(object):
    """The maildir plugin will save a feed item into a Maildir folder.

    The configuration is a little clunky, but it should be safe
    against hostile feeds.

    :param str to_addr: the email to use as "to" (defaults to
                        USER@localdomain)

    Example::

      [NASA breaking news]
      url = https://www.nasa.gov/rss/dyn/breaking_news.rss
      mailbox = ~/Maildir/
      folder = nasa
      args = me@example.com

    The above will save new feed items from the NASA feed into the
    ~/Maildir/nasa/ maildir folder, and will set the `To` field of the
    email to `me@example.com`.
    """

    def __init__(self, to_addr=None, feed=None, item=None, lock=None,
                 *args, **kwargs):
        msg, timestamp = make_message(feed=feed,
                                      item=item,
                                      to_addr=to_addr,
                                      cls=mailbox.MaildirMessage)
        msg.set_date(timestamp)
        prefix = os.path.expanduser(feed.get('mailbox', '~/Maildir'))
        utils.make_dirs_helper(prefix)
        folder = os.path.basename(os.path.abspath(utils.slug(feed.get('name'))))  # noqa
        # allow user to override our folder
        folder = feed.get('folder', folder)
        path = os.path.join(prefix, folder)
        logging.debug('established folder path %s', path)
        if lock:
            lock.acquire()
        maildir = mailbox.Maildir(path, create=True)
        self.key = maildir.add(msg)
        maildir.flush()
        if lock:
            lock.release()
        guid = item.get('guid', item.get('link', '???'))
        logging.info('saved item %s to %s',
                     guid, os.path.join(path, 'new', self.key))
