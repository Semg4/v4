
# -----------------------------------------------------------------------
def dz1(bot, chat_id):
    bot.send_message(chat_id, text="Готово")
# -----------------------------------------------------------------------
def dz2(bot, chat_id):
    bot.send_message(chat_id, text="Готово")
# -----------------------------------------------------------------------
def dz3(bot, chat_id):
    bot.send_message(chat_id, text="Готово")
# -----------------------------------------------------------------------
def dz4(bot, chat_id):
    bot.send_message(chat_id, text="Готово")
# -----------------------------------------------------------------------
def dz5(bot, chat_id):
    bot.send_message(chat_id, text="ДОДЕЛАТЬ")
# -----------------------------------------------------------------------
def dz6(bot, chat_id):
    proc_answer = lambda message: bot.send_message(chat_id, f"Добро пожаловать {message.text}! У тебя красивое имя, в нём {len(message.text)} букв!")
    my_input(bot, chat_id, "Как тебя зовут?", proc_answer)

# -----------------------------------------------------------------------
def my_input(bot, chat_id, txt, proc_answer):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, proc_answer)
# -----------------------------------------------------------------------