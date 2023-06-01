def select_keyboard(user_id, cnf):
    result = cnf.get_user_keyboard_info(user_id)
    kbd_size = result[0]
    kbd_switch = result[1]
    kbd_switch_force = result[2]
    result = cnf.get_keyboard_by_user_config(kbd_size, kbd_switch, kbd_switch_force)
    if result:
        if len(result) < 2:
            return result[0][0] + '\n' + result[0][1]
        else:
            list_of_keyboards = []
            for keyboard in result[0]:
                list_of_keyboards.append(keyboard)
            return list_of_keyboards
    else:
        return False
