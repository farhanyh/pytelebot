from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
import logging
import ipchecker
import database

class BotServer():
    """docstring for BotServer"""
    TOKEN = '661278652:AAG4enhNuePsOHJbfLN_Qgk0N0WlX7fdgPE'
    ADMIN_ID = 172522886

    def __init__(self):
        super(BotServer, self).__init__()
        self.run()

    def notifyIpUpdated(self):
        self.job_queue.run_once(self.notify_ip, 0)
        
    def start(self, bot, update):
        import model.user_model as user_model
        um = user_model.UserModel(self.db)
        sender = update.message.from_user
        res = um.get(sender.id)
        newreg = False
        if len(res) == 0:
            um.set(sender)
            newreg = True
        if update.message.chat.type == "group":
            bot.send_message(chat_id=update.message.chat_id, text="Reply me to send message to my creator.")
        else:
            msg = "Hello, " + sender.first_name + "! "
            if newreg:
                msg += "Nice to meet you."
            else:
                msg += "How can I help you today?"
            bot.send_message(chat_id=update.message.chat_id, text=msg)

    def echo(bot, update):
        sender = update.message.from_user
        if sender.id == BotServer.ADMIN_ID:
            bot.send_message(chat_id=update.message.chat_id, text="!"+update.message.text)
        else:
            bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
            sender_name = sender.username if sender.username else sender.first_name
            msg = "Message from: " + sender_name + ". Message: " + update.message.text
            bot.send_message(chat_id=BotServer.ADMIN_ID, text=msg)

    def caps(bot, update, args):
        text_caps = ' '.join(args).upper()
        bot.send_message(chat_id=update.message.chat_id, text=text_caps)

    def inline_caps(bot, update):
        query = update.inline_query.query
        if not query:
            return
        results = list()
        results.append(
            InlineQueryResultArticle(
                id=query.upper(),
                title='Caps',
                input_message_content=InputTextMessageContent(query.upper())
            )
        )
        bot.answer_inline_query(update.inline_query.id, results)

    def check_ip(self, bot, update):
        sender = update.message.from_user
        if sender.id == BotServer.ADMIN_ID:
            bot.send_message(chat_id=BotServer.ADMIN_ID, text=self.ipchecker.lastIP)
        else:
            bot.send_message(chat_id=update.message.chat_id, text="I'm sorry, this command is not available for you.")

    def notify_ip(self, bot, job):
        msg = "Home address has been changed: " + self.ipchecker.lastIP
        bot.send_message(chat_id=BotServer.ADMIN_ID, text=msg)

    def unknown(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

    def run(self):
        print("Starting server...")
        self.updater = Updater(token = BotServer.TOKEN)
        self.dispatcher = self.updater.dispatcher
        self.job_queue = self.updater.job_queue
        self.ipchecker = ipchecker.IPChecker(self)
        self.ipchecker.start()
        self.db = database.Database()
        self.db.connect()

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

        start_handler = CommandHandler('start', self.start)
        echo_handler = MessageHandler(Filters.text, BotServer.echo)
        caps_handler = CommandHandler('caps', BotServer.caps, pass_args=True)
        inline_caps_handler = InlineQueryHandler(BotServer.inline_caps)
        checkip_handler = CommandHandler('checkip', self.check_ip)
        unknown_handler = MessageHandler(Filters.command, BotServer.unknown)

        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(echo_handler)
        self.dispatcher.add_handler(caps_handler)
        self.dispatcher.add_handler(inline_caps_handler)
        self.dispatcher.add_handler(checkip_handler)
        self.dispatcher.add_handler(unknown_handler)

        print("Server started.")
        self.updater.start_polling()
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("Stopping server. Please wait...")
            self.db.close()
            self.ipchecker.join()
            self.updater.stop()
            print("Server stopped.")
