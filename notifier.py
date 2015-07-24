# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import feedparser
import time
import logging


class Notifier:
    addr = None
    notification_receiver = None
    update_time = None
    etag = None
    # Feed entries within this period will trigger notification
    check_period = 300

    def __init__(self, addr, notification_receiver=None):
        self.addr = addr
        if notification_receiver is None:
            notification_receiver = NotificationReceiver()
        self.notification_receiver = notification_receiver

    def scan_feed(self):
        feed = feedparser.parse(self.addr, etag=self.etag)
        logging.debug(feed)
        if feed.feed:
            self.etag = feed.etag
            if self.check_updated(feed.feed.updated_parsed):
                entry = self.cycle_entries(feed.entries)
                if entry:
                    self.notification_receiver.notify(entry)
        else:
            logging.debug("Feed not updated. Etag unchanged. %s" % self.etag)
        return False

    def cycle_entries(self, entries):
        for entry in entries:
            if self.entry_in_period(entry.published_parsed):
                logging.info("Error: %s" % entry.title)
                return entry
        return False

    def entry_in_period(self, date):
        logging.debug("time diff: %s - %s - %s" % (time.time(), time.mktime(date), time.timezone))
        time_diff = time.time() - time.mktime(date) - time.timezone
        logging.debug("time diff: %s" % time_diff)
        if time_diff < self.check_period:
            logging.debug("time diff: Less than %s" % self.check_period)
            return True
        logging.debug("time diff: Greater than %s" % self.check_period)
        return False

    def check_updated(self, update_time):
        if self.update_time is None or time.mktime(update_time) > time.mktime(self.update_time):
            logging.debug("update: %s" % time.strftime("%X %x", update_time))
            self.update_time = update_time
            return True
        logging.debug("update: no update found. Latest from %s" % time.strftime("%X %x", update_time))
        return False


class NotificationReceiver:
    def notify(self, entry):
        logging.info("Notification: received %s" % entry.title)
        logging.info("Notification: This received does nothing.")
