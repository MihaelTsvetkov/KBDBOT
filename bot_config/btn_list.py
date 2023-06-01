import telebot
from localization.json_translate import get_json_localization_buttons as jb

menu_btn_list = telebot.types.InlineKeyboardMarkup()
menu_btn_list.add(telebot.types.InlineKeyboardButton(text=jb("Наличие"), callback_data="availability"))
menu_btn_list.add(telebot.types.InlineKeyboardButton(text=jb("Ответы на вопросы"), callback_data="faq"))
menu_btn_list.add(telebot.types.InlineKeyboardButton(text=jb("Контакты"), callback_data="contacts"))
menu_btn_list.add(telebot.types.InlineKeyboardButton(text=jb("Подбор клавиатур"), callback_data="keyboard_selection"))
menu_btn_list.add(telebot.types.InlineKeyboardButton(text=jb("Отзывы"), callback_data="reviews"))

kbd_select_size = telebot.types.InlineKeyboardMarkup()
kbd_select_size.add(telebot.types.InlineKeyboardButton(text=jb("60%"), callback_data="small"))
kbd_select_size.add(telebot.types.InlineKeyboardButton(text=jb("TKL(80-87%)"), callback_data="tkl"))
kbd_select_size.add(telebot.types.InlineKeyboardButton(text=jb("full_size"), callback_data='full_size'))

kbd_select_switch_type = telebot.types.InlineKeyboardMarkup()
kbd_select_switch_type.add(telebot.types.InlineKeyboardButton(text=jb("Тактильные"), callback_data="tactile"))
kbd_select_switch_type.add(telebot.types.InlineKeyboardButton(text=jb("Линейные"), callback_data="linear"))
kbd_select_switch_type.add(telebot.types.InlineKeyboardButton(text=jb("Кликающие"), callback_data="clickers"))

kbd_switch_pressing_force = telebot.types.InlineKeyboardMarkup()
kbd_switch_pressing_force.add(telebot.types.InlineKeyboardButton(text=jb(">45g"), callback_data=">45"))
kbd_switch_pressing_force.add(telebot.types.InlineKeyboardButton(text=jb("45-60"), callback_data="45-60"))
kbd_switch_pressing_force.add(telebot.types.InlineKeyboardButton(text=jb(">60"), callback_data=">60"))

admin_panel_btn_list = telebot.types.InlineKeyboardMarkup()
admin_panel_btn_list.add(telebot.types.InlineKeyboardButton(text=jb("Добавить клавиатуру"),
                                                            callback_data="add_keyboard"))
admin_panel_btn_list.add(telebot.types.InlineKeyboardButton(text=jb("Список клавиатур"),
                                                            callback_data="list_of_keyboards"))
admin_panel_btn_list.add(telebot.types.InlineKeyboardButton(text=jb("Удалить клавиатуру"),
                                                            callback_data="delete_keyboard"))

back_btn = telebot.types.InlineKeyboardMarkup()
back_btn.add(telebot.types.InlineKeyboardButton(text=jb("Назад"), callback_data="back"))