import threading


class EmailThreadSend(threading.Thread):
    """
    Class to send email with multithreading.
    """

    def __init__(self, email_obj):
        threading.Thread.__init__(self)
        self.email_obj = email_obj

    def run(self):
        self.email_obj.send()
