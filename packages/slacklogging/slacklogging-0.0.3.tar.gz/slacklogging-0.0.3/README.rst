Logging Handler for Slack
=========================

You can log on Slack with this handler.


.. code-block:: python

   import logging

   import slacklogging


   slack_logger = logging.getLogger('slack')
   slack_logger.addHandler(slacklogging.Handler(token, channel, username))


You have to make a bot user for this logger, and need to invite the bot user to the channel.
