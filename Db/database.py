import psycopg2


class Database1:
    def __init__(self, host, port, user, password, dbname):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.prepare_database()
        self.query = ''

    def _get_connection(self):
        return psycopg2.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                database=self.dbname)

    def _get_connection_no_database(self):
        return psycopg2.connect(host=self.host, port=self.port, user=self.user, password=self.password)

    def create_database(self):
        connection = None
        try:
            connection = self._get_connection_no_database()
            connection.autocommit = True
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'kbd_republic'")
                exists = cursor.fetchone()
                if not exists:
                    cursor.execute('CREATE DATABASE kbd_republic')
        finally:
            connection.close()

    def create_table_keyboard_info(self):
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                query = """CREATE TABLE IF NOT EXISTS keyboard_info (
                                  keyboard_name VARCHAR(256),
                                  keyboard_size VARCHAR(4096),
                                  keyboard_switch_type VARCHAR(4096),
                                  keyboard_switch_force INTEGER,
                                  keyboard_photo VARCHAR(4096)
                                  ) """
                cursor.execute(query)
                connection.commit()

    def create_table_user_info(self):
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                query = """CREATE TABLE IF NOT EXISTS user_info (
                                  telegram_id INTEGER,
                                  user_name VARCHAR(256),
                                  is_admin INTEGER,
                                  keyboard_size VARCHAR(4096),
                                  keyboard_switch_type VARCHAR(4096),
                                  keyboard_switch_force INTEGER
                                  ) """
                cursor.execute(query)
                connection.commit()

    def prepare_database(self):
        self.create_table_keyboard_info()
        self.create_table_user_info()

    def add_user_keyboard_size(self, telegram_id, user_name, keyboard_size):
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                first_query = "SELECT telegram_id FROM user_info WHERE telegram_id = %s"
                first_val = (telegram_id,)
                cursor.execute(first_query, first_val)
                exists = cursor.fetchone()
                if not exists:
                    second_query = "INSERT INTO user_info " \
                                   "(telegram_id, user_name, keyboard_size) values(%s, %s, %s)"
                    second_val = (telegram_id, user_name, keyboard_size)
                    cursor.execute(second_query, second_val)
                else:
                    third_query = "UPDATE user_info SET user_name=%s, keyboard_size=%s where telegram_id = %s"
                    third_val = (user_name, keyboard_size, telegram_id)
                    cursor.execute(third_query, third_val)
        connection.commit()

    def add_user_keyboard_switch_type(self, telegram_id, keyboard_swittch_type):
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                query = "UPDATE user_info SET keyboard_switch_type=%s where telegram_id = %s"
                val = (keyboard_swittch_type, telegram_id)
                cursor.execute(query, val)
        connection.commit()

    def add_user_keyboard_switch_force(self, telegram_id, keyboard_switch_force):
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                query = "UPDATE user_info SET keyboard_switch_force = %s where telegram_id = %s"
                val = (keyboard_switch_force, telegram_id)
                cursor.execute(query, val)
        connection.commit()

    def get_user_keyboard_info(self, telegram_id):
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                query = "SELECT keyboard_size, keyboard_switch_type, keyboard_switch_force FROM user_info " \
                        "WHERE telegram_id=%s "
                val = (telegram_id,)
                cursor.execute(query, val)
                result = cursor.fetchone()
                if result:
                    return result
                else:
                    return False

    def get_keyboards(self):
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                query = "SELECT keyboard_name, keyboard_size, keyboard_photo, keyboard_switch_type," \
                        " keyboard_switch_force FROM keyboard_info"
                cursor.execute(query)
                result = cursor.fetchall()
                if result:
                    return result
                else:
                    return None

    def check_keyboard(self, kbd_name):
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                query = "SELECT keyboard_name FROM keyboard_info WHERE keyboard_name = %s"
                val = (kbd_name,)
                cursor.execute(query, val)
                result = cursor.fetchone()
                if result:
                    return result
                else:
                    return []

    def delete_keyboard_by_name(self, kbd_name):
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                query = "DELETE FROM keyboard_info WHERE keyboard_name = %s"
                val = (kbd_name,)
                cursor.execute(query, val)
        connection.commit()

    def get_keyboard_by_user_config(self, keyboard_size, keyboard_switch_type, keyboard_switch_force):
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                if keyboard_switch_force == '50':
                    query = "SELECT keyboard_name, keyboard_photo FROM keyboard_info " \
                            "WHERE keyboard_switch_force > 45 and keyboard_switch_force < 60 " \
                            "and keyboard_size = %s and keyboard_switch_type = %s"
                    val = (keyboard_size, keyboard_switch_type)
                    cursor.execute(query, val)
                    result = cursor.fetchall()
                    if result:
                        return result
                    else:
                        query = 'SELECT keyboard_name, keyboard_photo FROM keyboard_info WHERE ' \
                                'keyboard_switch_force > 45 and keyboard_switch_force < 60 and ' \
                                'keyboard_size = %s'
                        val = (keyboard_switch_type,)
                        cursor.execute(query, val)
                        result = cursor.fetchall()
                        if result:
                            return result
                        else:
                            query = 'SELECT keyboard_name, keyboard_photo FROM' \
                                    ' keyboard_info WHERE keyboard_switch_force > 45' \
                                    ' and keyboard_switch_force < 60 and keyboard_size = %s'
                            val = (keyboard_size,)
                            cursor.execute(query, val)
                            result = cursor.fetchall()
                            if result:
                                return result
                            else:
                                query = "SELECT keyboard_name, keyboard_photo FROM keyboard_info WHERE" \
                                        " keyboard_size = %s and keyboard_switch_type = %s"
                                val = (keyboard_size, keyboard_switch_type)
                                cursor.execute(query, val)
                                result = cursor.fetchall()
                                if result:
                                    return result
                                else:
                                    query = 'SELECT keyboard_name, keyboard_photo FROM keyboard_info' \
                                            ' WHERE keyboard_switch_force > 60 and keyboard_switch_type = %s'
                                    val = (keyboard_switch_type,)
                                    cursor.execute(query, val)
                                    result = cursor.fetchall()
                                    if result:
                                        return result
                                    else:
                                        query = 'SELECT keyboard_name, keyboard_photo FROM keyboard_info' \
                                                ' WHERE keyboard_switch_force > 45 and keyboard_size = %s'
                                        val = (keyboard_size,)
                                        cursor.execute(query, val)
                                        result = cursor.fetchall()
                                        if result:
                                            return result
                                        else:
                                            query = 'SELECT keyboard_name, keyboard_photo FROM keyboard_info ' \
                                                    'WHERE keyboard_switch_force > 45 and keyboard_size = %s' \
                                                    ' and keyboard_switch_type = %s'
                                            val = (keyboard_size, keyboard_switch_type)
                                            cursor.execute(query, val)
                                            result = cursor.fetchall()
                                            if result:
                                                return result
                                            else:
                                                query = 'SELECT keyboard_name, keyboard_photo FROM keyboard_info' \
                                                        ' WHERE keyboard_switch_force > 60 and keyboard_size = %s'
                                                val = (keyboard_size,)
                                                cursor.execute(query, val)
                                                result = cursor.fetchall()
                                                if result:
                                                    return result
                                                else:
                                                    query = 'SELECT keyboard_name, keyboard_photo FROM ' \
                                                            'keyboard_info WHERE keyboard_switch_force > 45 ' \
                                                            'and keyboard_switch_type = %s'
                                                    val = (keyboard_switch_type,)
                                                    cursor.execute(query, val)
                                                    result = cursor.fetchall()
                                                    if result:
                                                        return result
                                                    else:
                                                        query = 'SELECT keyboard_name, keyboard_photo FROM' \
                                                                ' keyboard_info WHERE keyboard_switch_force > 60' \
                                                                ' and keyboard_size = %s and keyboard_switch_type = %s'
                                                        val = (keyboard_size, keyboard_switch_type)
                                                        cursor.execute(query, val)
                                                        result = cursor.fetchall()
                                                        if result:
                                                            return result
                                                        else:
                                                            return None
                elif keyboard_switch_force == '45':
                    query = 'SELECT keyboard_name, keyboard_photo FROM keyboard_info WHERE keyboard_switch_force > 45 '\
                            'and keyboard_size = %s and keyboard_switch_type = %s'
                    val = (keyboard_size, keyboard_switch_type)
                    cursor.execute(query, val)
                    result = cursor.fetchall()
                    if result:
                        return result
                    else:
                        query = 'SELECT keyboard_name, keyboard_photo FROM' \
                                ' keyboard_info WHERE keyboard_switch_force > 45' \
                                ' and keyboard_switch_force < 60 and keyboard_size = %s ' \
                                'and keyboard_switch_type = %s'
                        val = (keyboard_size, keyboard_switch_type)
                        cursor.execute(query, val)
                        result = cursor.fetchall()
                        if result:
                            return result
                        else:
                            query = 'SELECT keyboard_name, keyboard_photo FROM keyboard_info WHERE ' \
                                    'keyboard_switch_force > 60 and keyboard_switch_type = %s ' \
                                    'and keyboard_size = %s'
                            val = (keyboard_switch_type, keyboard_size)
                            cursor.execute(query, val)
                            result = cursor.fetchall()
                            if result:
                                return result
                            else:
                                query = 'SELECT keyboard_name, keyboard_photo FROM keyboard_info WHERE ' \
                                        'keyboard_switch_force > 45 and keyboard_switch_force < 60 and ' \
                                        'keyboard_size = %s'
                                val = (keyboard_size, )
                                cursor.execute(query, val)
                                result = cursor.fetchall()
                                if result:
                                    return result
                                else:
                                    query = 'SELECT keyboard_name, keyboard_photo FROM keyboard_info ' \
                                            'WHERE keyboard_switch_force > 45 and keyboard_switch_force < 60 ' \
                                            'and keyboard_switch_type = %s'
                                    val = (keyboard_switch_type,)
                                    cursor.execute(query, val)
                                    result = cursor.fetchall()
                                    if result:
                                        return result
                                    else:
                                        query = 'SELECT keyboard_name, keyboard_photo FROM keyboard_info' \
                                                ' WHERE keyboard_switch_force > 45 and keyboard_size = %s'
                                        val = (keyboard_size,)
                                        cursor.execute(query, val)
                                        result = cursor.fetchall()
                                        if result:
                                            return result
                                        else:
                                            query = 'SELECT keyboard_name, keyboard_photo FROM keyboard_info' \
                                                    ' WHERE keyboard_switch_force > 45 and keyboard_switch_type = %s'
                                            val = (keyboard_switch_type,)
                                            cursor.execute(query, val)
                                            result = cursor.fetchall()
                                            if result:
                                                return result
                                            else:
                                                query = 'SELECT keyboard_name, keyboard_photo FROM keyboard_info' \
                                                        ' WHERE keyboard_switch_force > 60 and keyboard_size = %s'
                                                val = (keyboard_size,)
                                                cursor.execute(query, val)
                                                result = cursor.fetchall()
                                                if result:
                                                    return result
                                                else:
                                                    query = "SELECT keyboard_name, keyboard_photo FROM keyboard_info" \
                                                            " WHERE keyboard_size = %s and keyboard_switch_type = %s"
                                                    val = (keyboard_size, keyboard_switch_type)
                                                    cursor.execute(query, val)
                                                    result = cursor.fetchall()
                                                    if result:
                                                        return result
                                                    else:
                                                        query = 'SELECT keyboard_name, keyboard_photo FROM' \
                                                                ' keyboard_info WHERE and keyboard_switch_force > 60 ' \
                                                                'and keyboard_switch_type = %s'
                                                        val = (keyboard_switch_type,)
                                                        cursor.execute(query, val)
                                                        result = cursor.fetchall()
                                                        if result:
                                                            return result
                                                        return None
                elif keyboard_switch_force == '60':
                    query = 'SELECT keyboard_name, keyboard_photo FROM keyboard_info ' \
                            'WHERE keyboard_switch_force > 60 and keyboard_size = %s and keyboard_switch_type = %s'
                    val = (keyboard_size, keyboard_switch_type)
                    cursor.execute(query, val)
                    result = cursor.fetchall()
                    if result:
                        return result
                    else:
                        query = 'SELECT keyboard_name, keyboard_photo FROM keyboard_info ' \
                                'WHERE keyboard_switch_force > 45 and keyboard_switch_force < 60 ' \
                                'and keyboard_size = %s and keyboard_switch_type = %s'
                        val = (keyboard_size, keyboard_switch_type)
                        cursor.execute(query, val)
                        result = cursor.fetchall()
                        if result:
                            return result
                        else:
                            query = 'SELECT keyboard_name, keyboard_photo FROM keyboard_info WHERE ' \
                                    'keyboard_switch_force > 45 and keyboard_size = %s and keyboard_switch_type = %s'
                            val = (keyboard_size, keyboard_switch_type)
                            cursor.execute(query, val)
                            result = cursor.fetchall()
                            if result:
                                return result
                            else:
                                query = "SELECT keyboard_name, keyboard_photo FROM keyboard_info WHERE " \
                                        "keyboard_size = %s and keyboard_switch_type = %s"
                                val = (keyboard_size, keyboard_switch_type)
                                cursor.execute(query, val)
                                result = cursor.fetchall()
                                if result:
                                    return result
                                else:
                                    query = 'SELECT keyboard_name, keyboard_photo FROM keyboard_info' \
                                            ' WHERE keyboard_switch_force > 60 and keyboard_switch_type = %s'
                                    val = (keyboard_switch_type,)
                                    cursor.execute(query, val)
                                    result = cursor.fetchall()
                                    if result:
                                        return result
                                    else:
                                        query = 'SELECT keyboard_name, keyboard_photo FROM keyboard_info' \
                                                ' WHERE keyboard_switch_force > 60 and keyboard_size = %s'
                                        val = (keyboard_size,)
                                        cursor.execute(query, val)
                                        result = cursor.fetchall()
                                        if result:
                                            return result
                                        else:
                                            query = 'SELECT keyboard_name, keyboard_photo FROM keyboard_info' \
                                                   ' WHERE keyboard_switch_force > 45 and keyboard_size = %s'
                                            val = (keyboard_size,)
                                            cursor.execute(query, val)
                                            result = cursor.fetchall()
                                            if result:
                                                return result
                                            else:
                                                query = 'SELECT keyboard_name, keyboard_photo FROM ' \
                                                        'keyboard_info WHERE keyboard_switch_force > 45 ' \
                                                        'and keyboard_switch_type = %s'
                                                val = (keyboard_switch_type,)
                                                cursor.execute(query, val)
                                                result = cursor.fetchall()
                                                if result:
                                                    return result
                                                else:
                                                    query = 'SELECT keyboard_name, keyboard_photo FROM keyboard_info ' \
                                                            'WHERE keyboard_switch_force > 45 and ' \
                                                            'keyboard_switch_force < 60 and ' \
                                                            'keyboard_size = %s'
                                                    val = (keyboard_size,)
                                                    cursor.execute(query, val)
                                                    result = cursor.fetchall()
                                                    if result:
                                                        return result
                                                    else:
                                                        query = 'SELECT keyboard_name, keyboard_photo FROM ' \
                                                                'keyboard_info WHERE keyboard_switch_force > 45 ' \
                                                                'and keyboard_switch_force < 60 and ' \
                                                                'keyboard_switch_type = %s'
                                                        val = (keyboard_switch_type,)
                                                        cursor.execute(query, val)
                                                        result = cursor.fetchall()
                                                        if result:
                                                            return result
                                                        else:
                                                            return None


    def add_keyboard_by_admin(self, kbd_name, kbd_size, kbd_switch_type, kbd_switch_force, kbd_photo):
        with self._get_connection() as connection:
            with connection.cursor() as cursor:
                query = "INSERT INTO keyboard_info (keyboard_name, keyboard_size, keyboard_switch_type, " \
                        "keyboard_switch_force, keyboard_photo) values(%s, %s, %s, %s, %s)"
                val = (kbd_name, kbd_size, kbd_switch_type, kbd_switch_force, kbd_photo)
                cursor.execute(query, val)
        connection.commit()
