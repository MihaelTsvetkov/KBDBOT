from selection import select_keyboard
from btn_list import kbd_select_size, kbd_select_switch_type, menu_btn_list, kbd_switch_pressing_force
from localization.json_translate import get_json_localization
import logging
logger = logging.getLogger(__name__)


class UserFSM:
    def __init__(self, bot, process_message, config):
        self.state = None
        self.bot = bot
        self.config = config
        self.process_message = process_message
        self.switch_force = None

    def start_command(self, call):
        self.start(call)

    def run_user(self, call):
        self.state(call)

    def start(self, call):
        self.bot.send_message(call.from_user.id, get_json_localization("Приветствие"),
                              reply_markup=menu_btn_list, parse_mode="Markdown")
        self.state = self.menu

    def menu(self, call):
        try:
            if call.data == "availability":
                result = self.config.get_keyboards()
                if not result:
                    self.bot.send_message(call.from_user.id, get_json_localization("Наличие"))
                else:
                    for tuples in result:
                        keyboard = get_json_localization("Клавиатура") + f"{tuples[0]}\n" + \
                                   get_json_localization("Размер") + f"{tuples[1]}\n" + \
                                   get_json_localization("Тип переключателей") + \
                                   f"{tuples[3]}\n" + get_json_localization("Усилие на свитчи") + f"{tuples[4]}" + \
                                   get_json_localization("unit") + f"\n{tuples[2]}"
                        self.bot.send_message(call.from_user.id, keyboard)

            elif call.data == "faq":
                self.bot.send_message(call.from_user.id, get_json_localization("FAQ"))

            elif call.data == "contacts":
                self.bot.send_message(call.from_user.id, get_json_localization("Контакты"))

            elif call.data == "reviews":
                self.bot.send_message(call.from_user.id, get_json_localization("Отзывы"))

            elif call.data == "keyboard_selection":
                self.bot.delete_message(call.from_user.id, call.message.message_id)
                self.bot.send_message(call.from_user.id, get_json_localization("Выберите размер"),
                                      reply_markup=kbd_select_size)
                self.state = self.keyboard_size_selection
        except AttributeError:
            pass

    def keyboard_size_selection(self, call):
        if call.data == "small" or call.data == "tkl" or call.data == "full_size":
            self.config.add_user_keyboard_size(call.from_user.id, call.from_user.username, call.data)
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id, get_json_localization("Выберите тип переключателей"),
                                  reply_markup=kbd_select_switch_type)
            self.state = self.keyboard_switch_type_selection

    def keyboard_switch_type_selection(self, call):
        if call.data == "tactile" or call.data == "linear" or call.data == "clickers":
            self.config.add_user_keyboard_switch_type(call.from_user.id, call.data)
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            self.bot.send_message(call.from_user.id, get_json_localization("Выберите силу нажатия переключателей"),
                                  reply_markup=kbd_switch_pressing_force)
            self.state = self.keyboard_switch_pressing_force_selection

    def keyboard_switch_pressing_force_selection(self, call):
        if call.data == ">45" or call.data == "45-60" or call.data == ">60":
            if call.data == ">45":
                self.switch_force = 45
            elif call.data == '45-60':
                self.switch_force = 50
            elif call.data == '<60':
                self.switch_force = 60

            self.config.add_user_keyboard_switch_force(call.from_user.id, self.switch_force)
            self.bot.delete_message(call.from_user.id, call.message.message_id)
            message = self.bot.send_message(call.from_user.id, get_json_localization("Подбор вариантов"))
            result = select_keyboard(call.from_user.id, self.config)
            if result:
                if len(result) < 1:
                    self.bot.delete_message(call.from_user.id, message.message_id)
                    self.bot.send_message(call.from_user.id,
                                          get_json_localization("Подходят клавиатуры") + result)
                else:
                    self.bot.delete_message(call.from_user.id, message.message_id)
                    self.bot.send_message(call.from_user.id, get_json_localization("Подходит клавиатура") + result)
            else:
                self.bot.delete_message(call.from_user.id, message.message_id)
                self.bot.send_message(call.from_user.id, get_json_localization("Не найдено клавиатур"))

    def is_finished_user(self):
        return self.state is None
