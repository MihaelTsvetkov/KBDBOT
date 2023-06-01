from btn_list import back_btn
from authorized import Authorized
from btn_list import admin_panel_btn_list
from localization.json_translate import get_json_localization
from options import settings


class AdminFSM:
    def __init__(self, bot, config, process_message):
        self.config = config
        self.process_message = process_message
        self.state = None
        self.bot = bot
        self.kbd_size = None
        self.kbd_name = None
        self.kbd_switch_type = None
        self.kbd_switch_force = None
        self.kbd_photo = None
        self.message = None

    def start_admin(self, call):
        self.bot.send_message(call.from_user.id, get_json_localization("Введите пароль"))
        self.state = self.authorized

    def run_admin(self, call):
        self.state(call)

    def authorized(self, call):
        auth = Authorized(settings.ADMIN_PASSWORD)
        true_pass = auth.check_password(call.text)
        if not true_pass:
            self.bot.send_message(call.from_user.id, get_json_localization("Введите пароль"))
        else:
            self.bot.send_message(call.from_user.id, get_json_localization("Добро пожаловать в админ панель"),
                                  reply_markup=admin_panel_btn_list)
            self.state = self.admin_panel

    def admin_panel(self, call):
        if not hasattr(call, "data"):
            pass
        else:
            if call.data == "add_keyboard":
                self.bot.delete_message(call.from_user.id, call.message.id)
                self.message = self.bot.send_message(call.from_user.id,
                                                     get_json_localization("Введите размер клавиатуры"),
                                                     reply_markup=back_btn)
                self.state = self.admin_panel_add_keyboard_size

            if call.data == 'list_of_keyboards':
                result = self.admin_panel_get_keyboards()
                for keyboard in result:
                    self.bot.send_message(call.from_user.id, keyboard)

            if call.data == "delete_keyboard":
                self.bot.delete_message(call.from_user.id, call.message.id)
                self.message = self.bot.send_message(call.from_user.id,
                                                     get_json_localization("Введите размер клавиатуры"))
                self.state = self.delete_keyboard

    def delete_keyboard(self, call):
        kbd = call.text
        if not self.config.check_keyboard(kbd):
            self.bot.send_message(call.from_user.id, get_json_localization("Такой клавиатуры не существует"))
        else:
            self.config.delete_keyboard_by_name(kbd)
            self.bot.delete_message(call.from_user.id, self.message.message_id)
            self.bot.send_message(call.from_user.id, get_json_localization("Клавиатура успешно удалена"))

    def admin_panel_get_keyboards(self):
        result = self.config.get_keyboards()
        list_of_keyboards = []
        for tuples in result:
            keyboard = get_json_localization("Клавиатура") + f"{tuples[0]}\n" + get_json_localization("Размер") + \
                       f"{tuples[1]}\n" + get_json_localization("Тип переключателей") + f"{tuples[3]}\n" + \
                       get_json_localization("Усилие на свитчи") + f"{tuples[4]}" + get_json_localization("unit") + \
                       f"\n{tuples[2]}"

            list_of_keyboards.append(keyboard)
        return list_of_keyboards

    def admin_panel_add_keyboard_size(self, call):
        if not hasattr(call, "text"):
            if call.data == 'back':
                self.bot.delete_message(call.from_user.id, call.message.id)
                self.bot.send_message(call.from_user.id, get_json_localization("Добро пожаловать в админ панель"),
                                      reply_markup=admin_panel_btn_list)
                self.state = self.admin_panel
                return
        else:
            self.kbd_size = call.text
            self.bot.delete_message(call.chat.id, self.message.message_id)
            self.message = self.bot.send_message(call.from_user.id,
                                                 get_json_localization("Введите название клавиатуры"),
                                                 reply_markup=back_btn)
            self.state = self.admin_panel_add_keyboard_name

    def admin_panel_add_keyboard_name(self, call):
        if not hasattr(call, "text"):
            if call.data == 'back':
                self.kbd_size = None
                self.bot.delete_message(call.from_user.id, self.message.message_id)
                self.message = self.bot.send_message(call.from_user.id,
                                                     get_json_localization("Введите размер клавиатуры"),
                                                     reply_markup=back_btn)
                self.state = self.admin_panel_add_keyboard_size
                return
        else:
            self.kbd_name = call.text
            self.bot.delete_message(call.from_user.id, self.message.message_id)
            self.message = self.bot.send_message(call.from_user.id,
                                                 get_json_localization("Введите тип переключателей"),
                                                 reply_markup=back_btn)
            self.state = self.admin_panel_add_switch_type

    def admin_panel_add_switch_type(self, call):
        if not hasattr(call, "text"):
            if call.data == 'back':
                self.kbd_name = None
                self.bot.delete_message(call.from_user.id, self.message.message_id)
                self.message = self.bot.send_message(call.from_user.id,
                                                     get_json_localization("Введите название клавиатуры"),
                                                     reply_markup=back_btn)
                self.state = self.admin_panel_add_keyboard_name
                return
        else:
            self.kbd_switch_type = call.text
            self.bot.delete_message(call.from_user.id, self.message.message_id)
            self.message = self.bot.send_message(call.from_user.id,
                                                 get_json_localization("Введите силу нажатия переключателей"),
                                                 reply_markup=back_btn)
            self.state = self.admin_panel_add_switch_force

    def admin_panel_add_switch_force(self, call):
        if not hasattr(call, "text"):
            if call.data == 'back':
                self.kbd_switch_type = None
                self.bot.delete_message(call.from_user.id, self.message.message_id)
                self.message = self.bot.send_message(call.from_user.id,
                                                     get_json_localization("Введите тип переключателей"),
                                                     reply_markup=back_btn)
                self.state = self.admin_panel_add_switch_type
                return
        else:
            self.kbd_switch_force = call.text
            self.bot.delete_message(call.from_user.id, self.message.message_id)
            self.message = self.bot.send_message(call.from_user.id,
                                                 get_json_localization("Введите ссылку на фотографию с клавиатурой"),
                                                 reply_markup=back_btn)
            self.state = self.admin_panel_add_keyboard_photo

    def admin_panel_add_keyboard_photo(self, call):
        if not hasattr(call, "text"):
            if call.data == 'back':
                self.kbd_switch_force = None
                self.bot.delete_message(call.from_user.id, self.message.message_id)
                self.message = self.bot.send_message(call.from_user.id,
                                                     get_json_localization("Введите силу нажатия переключателей"),
                                                     reply_markup=back_btn)
                self.state = self.admin_panel_add_switch_force
                return
        else:
            self.bot.delete_message(call.from_user.id, self.message.message_id)
            self.bot.send_message(call.from_user.id, get_json_localization("Клавиатура успешно удалена"),
                                  reply_markup=admin_panel_btn_list)
            self.kbd_photo = call.text
            self.config.add_keyboard_by_admin(self.kbd_name, self.kbd_size, self.kbd_switch_type, self.kbd_switch_force,
                                              self.kbd_photo)
            self.kbd_name = None
            self.kbd_switch_type = None
            self.kbd_switch_force = None
            self.kbd_photo = None
            self.state = self.admin_panel

    def is_finished_admin(self):
        return self.state is None
