# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
"""New Relic Alert Notifier

Usage:
    app.py run
    app.py test

-h --help    show this
"""

import logging
import lazybone_receiver
import notifier
import time
from docopt import docopt
from collections import namedtuple

logging.basicConfig(level=logging.DEBUG)

addr = '' 

def run():
    notification_receiver = lazybone_receiver.LazyboneReceiver()
    new_relic_notifier = notifier.Notifier(addr, notification_receiver)
    while 1:
        if new_relic_notifier.scan_feed():
            logging.info("Scan found alert!")
        else:
            time.sleep(60)


def test():
    feed = namedtuple("feed", "title")
    feed.title = "test notification"
    notification_receiver = lazybone_receiver.LazyboneReceiver()
    notification_receiver.notify(feed)    


if __name__ == '__main__':
    arguments = docopt(__doc__)
    if arguments["run"]:
        run()
    elif arguments['test']:
        test()
