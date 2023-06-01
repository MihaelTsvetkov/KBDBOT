from Db.database import Database1


class Config:
    def __init__(self, db: Database1):
        self.db = db

    def add_user_keyboard_size(self, telegram_id, user_name, keyboard_size):
        return self.db.add_user_keyboard_size(telegram_id, user_name, keyboard_size)

    def add_user_keyboard_switch_type(self, telegram_id, keyboard_swittch_type):
        return self.db.add_user_keyboard_switch_type(telegram_id, keyboard_swittch_type)

    def add_user_keyboard_switch_force(self, telegram_id, keyboard_switch_force):
        return self.db.add_user_keyboard_switch_force(telegram_id, keyboard_switch_force)

    def get_user_keyboard_info(self, telegram_id):
        return self.db.get_user_keyboard_info(telegram_id)

    def get_keyboard_by_user_config(self, keyboard_size, keyboard_switch_type, keyboard_switch_force):
        return self.db.get_keyboard_by_user_config(keyboard_size, keyboard_switch_type, keyboard_switch_force)

    def add_keyboard_by_admin(self, kbd_name, kbd_size, kbd_switch_type, kbd_switch_force, kbd_photo):
        return self.db.add_keyboard_by_admin(kbd_name, kbd_size, kbd_switch_type, kbd_switch_force, kbd_photo)

    def get_keyboards(self):
        return self.db.get_keyboards()

    def check_keyboard(self, kbd_name):
        return self.db.check_keyboard(kbd_name)

    def delete_keyboard_by_name(self, kbd_name):
        return self.db.delete_keyboard_by_name(kbd_name)