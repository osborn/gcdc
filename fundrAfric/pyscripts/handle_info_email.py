import logging
import webapp2
from google.appengine.api import mail
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Received a message from: " + mail_message.sender)
        message = mail.EmailMessage(sender="Example Support <" + mail_message.sender + ">",
                            subject="Message through app engine")
        message.to = "Christian <christian.osei-bonsu@meltwater.org>"
        message.body = """
        Dear Albert:

        Your example.com account has been approved.  You can now visit
        http://www.example.com/ and sign in using your Google Account to
        access new features.

        Please let us know if you have any questions.

        The example.com Team
        """

        message.send()

app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)