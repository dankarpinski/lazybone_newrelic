# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import time
import logging
import lazybone
import notifier
import sys
import signal


class LazyboneReceiver(notifier.NotificationReceiver):
    lazybone = None
    # Seconds to enable lazybone for
    flash_period = 60

    def __init__(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        self.lazybone = lazybone.Lazybone()
        logging.info("Connecting Lazybone")
        if self.lazybone.connect_bluetooth_bee() is not True:
            logging.info("Lazybone device could not be found!")
            sys.exit(1)

    def signal_handler(self, signal, frame):
        self.disable_light()
        self.close()
        sys.exit(0)

    def notify(self, entry):
        logging.info("Notification: received %s" % entry.title)
        self.flash_light(self.flash_period)

    def enable_light(self):
        self.lazybone.on()

    def disable_light(self):
        self.lazybone.off()

    def close(self):
        self.lazybone.close()

    def flash_light(self, duration):
        logging.debug("Notification: Flashing Light for %s seconds" % duration)
        self.lazybone.on()
        time.sleep(duration)
        self.lazybone.off()
