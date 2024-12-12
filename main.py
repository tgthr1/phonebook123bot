
import json
import telebot as tb
from dotenv import load_dotenv
import os
import sys
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from abc import ABC, abstractmethod

class AbstractUser(ABC):
    @abstractmethod
    def __init__(self, name, phone_number, features): pass

class AbstractTUser(ABC):
    @abstractmethod
    def __init__(self, id, tag): pass

class AbstractDatabase(ABC):
    @abstractmethod
    def __init__(self, path): pass

    @abstractmethod
    
    def save_user(self, user, id: int):  pass 

    @abstractmethod
    def lower_features(self, features): pass

    
    @abstractmethod
    def get_user(self, user, id: int): pass

    @abstractmethod
    def rewrite_all_data(self, data): pass

    
    @abstractmethod
    def delete_user(self, user, id: int): pass

   
    @abstractmethod
    def get_data(self) -> dict: pass


class User(AbstractUser):
    def __init__(self, name="", phone_number="", features=""):
        self.name = name
        self.phone_number = phone_number
        self.features = features 


class TUser(AbstractTUser):
    def __init__(self, id, tag):
        
        self.id = id
        self.tag = tag

        self.working_user = User() 

        
        self._adding_user_name = False
        self._adding_user_phone_number = False
        self._adding_user_features = False
        self._deleting_user_name = False
        self._deleting_user_phone = False
        self._deleting_user_features = False
        self._finding_user_name = False
        self._finding_user_phone = False
        self._finding_user_features = False
        self._getting_data = False


class Database(AbstractDatabase):
    def __init__(self, path):
        self.path = path

    
    def save_user(self, user: User, id: int):  
        all_data = self.get_data()
        id = str(id)
        with open(self.path, 'w') as f:
            try:
                all_data[id].append(user.__dict__)
            except:
                
                all_data[id] = []
                all_data[id].append(user.__dict__)
            data = json.dumps(all_data, indent=4)
            f.write(data)

    def lower_features(self, features):
        result = []
        for ft in features:
            result.append(ft.lower())
        return result

    
    def get_user(self, user: User, id: int):
        with open(self.path, 'r') as f:
            data = json.loads(f.read())
            current_user = data.get(str(id)) 
       
        for person in current_user:
            if person == user.__dict__:
                return User(person["name"], person["phone_number"], person["features"])

       
        for person in current_user:
            if person["name"].lower() == user.__dict__["name"].lower() and person["phone_number"] == user.__dict__["phone_number"]:
                return User(person["name"], person["phone_number"], person["features"])
            elif person["phone_number"] == user.__dict__["phone_number"] and self.lower_features(person["features"]) == self.lower_features(user.__dict__[
                "features"]):
                return User(person["name"], person["phone_number"], person["features"])
            elif person["name"].lower() == user.__dict__["name"].lower() and self.lower_features(person["features"]) == self.lower_features(user.__dict__["features"]):
                return User(person["name"], person["phone_number"], person["features"])

        
        for person in current_user:
            if person["phone_number"] == user.__dict__["phone_number"]:
                return User(person["name"], person["phone_number"], person["features"])

       
        for person in current_user:
            if self.lower_features(person["features"]) == self.lower_features(user.__dict__["features"]):
                return User(person["name"], person["phone_number"], person["features"])

        
        for person in current_user:
            if person["name"].lower() == user.__dict__["name"].lower():
                return User(person["name"], person["phone_number"], person["features"])

        return None

    def rewrite_all_data(self, data):
        with open(self.path, 'w') as f:
            data = json.dumps(data, indent=4)
            f.write(data)

    
    def delete_user(self, user: User, id: int):
        with open(self.path, 'r') as f:
            data = json.loads(f.read())
            current_user = data.get(str(id))  
            
            for person in current_user:
                if person == user.__dict__:
                    deleted = current_user.pop(current_user.index(person))
                    self.rewrite_all_data(data)
                    return deleted

            
            for person in current_user:
                if person["name"].lower() == user.__dict__["name"].lower() and person["phone_number"] == user.__dict__[
                    "phone_number"]:
                    deleted = current_user.pop(current_user.index(person))
                    self.rewrite_all_data(data)
                    return deleted
                elif person["phone_number"] == user.__dict__["phone_number"] and self.lower_features(
                        person["features"]) == self.lower_features(user.__dict__[
                                                                       "features"]):
                    deleted = current_user.pop(current_user.index(person))
                    self.rewrite_all_data(data)
                    return deleted
                elif person["name"].lower() == user.__dict__["name"].lower() and self.lower_features(
                        person["features"]) == self.lower_features(user.__dict__["features"]):
                    deleted = current_user.pop(current_user.index(person))
                    self.rewrite_all_data(data)
                    return deleted

            
            for person in current_user:
                if person["phone_number"] == user.__dict__["phone_number"]:
                    deleted = current_user.pop(current_user.index(person))
                    self.rewrite_all_data(data)
                    return deleted

           
            for person in current_user:
                if self.lower_features(person["features"]) == self.lower_features(user.__dict__["features"]):
                    deleted = current_user.pop(current_user.index(person))
                    self.rewrite_all_data(data)
                    return deleted

           
            for person in current_user:
                if person["name"].lower() == user.__dict__["name"].lower():
                    deleted = current_user.pop(current_user.index(person))
                    self.rewrite_all_data(data)
                    return deleted
        return None 

    
    def get_data(self) -> dict:
        with open(self.path, 'r') as f:
            data = json.loads(f.read())
            return data

if __name__ == "__main__":
    load_dotenv("tokens.env")
    TOKEN = os.getenv("PHONE_BOOK_TOKEN")
    bot = tb.TeleBot(TOKEN)

    tusers = dict() 

    db = Database('database.json')
else:
    sys.exit(0)

@bot.message_handler(commands=['start'])
def start_bot(msg):
    global tusers
    bot.send_message(msg.chat.id, f"Привет {msg.chat.first_name}! "
                                  f"Это бот который поможет тебе управлять собственной виртуальной книгой контактов!"
                                  f"Просто следуй инструкциям на кнопках для того, чтобы управлять контактами :)")
    tusers[msg.chat.id] = TUser(msg.chat.id, msg.chat.username)
    create_main_buttons(msg.chat.id)

def create_main_buttons(id):
   
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    add_user_btn = KeyboardButton("Добавить человека")
    show_users_btn = KeyboardButton("Просмотреть книгу контактов")
    delete_user_btn = KeyboardButton("Удалить человека из книги контактов")
    find_user_btn = KeyboardButton("Найти человека")
    markup.add(add_user_btn, delete_user_btn, find_user_btn, show_users_btn)

    bot.send_message(id, text="Выберите варианты:", reply_markup=markup)

@bot.message_handler(content_types=["text"])
def main_handler(msg):
    global tusers
    try:
        tuser = tusers[msg.chat.id]
    except KeyError:
        tusers[msg.chat.id] = TUser(msg.chat.id, msg.chat.username)
        tuser = tusers[msg.chat.id]
    if msg.text == "Добавить человека" or msg.text == "/add_user":
        restart_tuser_flags(tuser)
        add_user_name(tuser)
    elif msg.text == "Просмотреть книгу контактов" or msg.text == "/get_user_data":
        restart_tuser_flags(tuser)
        get_data(tuser)
    elif msg.text == "Удалить человека из книги контактов" or msg.text == "/delete_user":
        restart_tuser_flags(tuser)
        delete_user_name(tuser)
    elif msg.text == "Найти человека" or msg.text == "/find_user":
        restart_tuser_flags(tuser)
        find_user_name(tuser)
    else:
        command(msg, tuser)

def restart_tuser_flags(tuser: TUser):
    tuser.working_user = User()
    tuser._adding_user_name = False
    tuser._adding_user_phone_number = False
    tuser._adding_user_features = False
    tuser._deleting_user_name = False
    tuser._deleting_user_phone = False
    tuser._deleting_user_features = False
    tuser._finding_user_name = False
    tuser._finding_user_phone = False
    tuser._finding_user_features = False
    tuser._getting_data = False


def command(msg, tuser: TUser):
    if tuser._adding_user_name: 
        tuser.working_user.name = msg.text.strip()
        tuser._adding_user_name = False
        add_user_phone(tuser)
    elif tuser._adding_user_phone_number: 
        if check_phone_number(msg.text.strip()): 
            tuser.working_user.phone_number = msg.text.strip()
            tuser._adding_user_phone_number = False
            add_user_features(tuser)
        else:
            bot.send_message(tuser.id, "Не правильно набран номер!\nВведите его ещё раз:")
    elif tuser._adding_user_features: 
        tuser.working_user.features = msg.text.split()
        tuser._adding_user_features = False
        
        db.save_user(tuser.working_user, tuser.id)
        restart_tuser_flags(tuser)
    elif tuser._deleting_user_name: 
        tuser.working_user.name = msg.text.strip()
        tuser._deleting_user_name = False
        delete_user_phone(tuser)
    elif tuser._deleting_user_phone: 
        tuser.working_user.phone_number = msg.text.strip()
        tuser._deleting_user_phone = False
        delete_user_features(tuser)
    elif tuser._deleting_user_features: 
        tuser.working_user.features = msg.text.strip()
        tuser._deleting_user_features = False
        deleted = db.delete_user(tuser.working_user, tuser.id)
        if not deleted:
            bot.send_message(tuser.id, "Удалить не получилось, так как такого человека в книге контактов нет(")
            create_main_buttons(tuser.id)
        else:
            bot.send_message(tuser.id, "Человек успешно удалён!")
            create_main_buttons(tuser.id)
        restart_tuser_flags(tuser)
    elif tuser._finding_user_name: 
        tuser.working_user.name = msg.text.strip()
        tuser._finding_user_name = False
        find_user_phone(tuser)
    elif tuser._finding_user_phone:
        tuser.working_user.phone_number = msg.text.strip()
        tuser._finding_user_phone = False
        find_user_features(tuser)
    elif tuser._finding_user_features:
        tuser.working_user.features = msg.text.strip()
        tuser._finding_user_features = False

        user_data = db.get_user(tuser.working_user, tuser.id)

        if user_data:
            result = f"Имя: {user_data.name.capitalize()}\nНомер телефона: {user_data.phone_number}"
            if user_data.features: result += f"\n{", ".join(user_data.features)}"
            bot.send_message(tuser.id, result)
        else:
            bot.send_message(tuser.id, "Не нашлось такого человека :(\nПопробуйте ввести данные заново...")
            create_main_buttons(tuser.id)
        restart_tuser_flags(tuser)
    else:
        bot.send_message(tuser.id, "Такая команда не найдена, пожалуйста...")
create_main_buttons(tuser.id)
restart_tuser_flags(tuser)


def check_phone_number(number):
    if number[0] == "+" and number[1:].isdigit():
        return True
    elif number.isdigit():
        return True
    
    return False

def add_user_name(tuser: TUser):
    tuser._adding_user_name = True
    bot.send_message(tuser.id, "Напишите имя того человека, которого вы хотите добавить в базу:")

def add_user_phone(tuser: TUser):
    tuser._adding_user_phone_number = True
    bot.send_message(tuser.id, "Напишите номер телефона того человека, которого вы хотите добавить в базу:")

def add_user_features(tuser: TUser):
    tuser._adding_user_features = True
    bot.send_message(tuser.id, "Напишите через пробел уникальные особенности человека, которого вы хотите добавить, это нужно чтобы вы могли различать людей с одинаковыми именами:")

def delete_user_name(tuser: TUser):
    tuser._deleting_user_name = True
    bot.send_message(tuser.id, "Напишите имя человека, которого вы хотите удалить из книги контактов:")

def delete_user_phone(tuser: TUser):
    tuser._deleting_user_phone = True
    bot.send_message(tuser.id, "Напишите номер телефона человека, которого вы хотите удалить (это необязательно):")

def delete_user_features(tuser: TUser):
    tuser._deleting_user_features = True
    bot.send_message(tuser.id, "Напишите через пробел уникальные черты человека, которого вы хотите удалить (это необязательно):")

def find_user_name(tuser):
    tuser._finding_user_name = True
    bot.send_message(tuser.id, "Напишите имя человека, которого вы хотите найти в книге контактов:")

def find_user_phone(tuser):
    tuser._finding_user_phone = True
    bot.send_message(tuser.id, "Напишите номер телефона человека, которого вы хотите найти в книге контактов:")

def find_user_features(tuser):
    tuser._finding_user_features = True
    bot.send_message(tuser.id, "Напишите через пробел уникальные черты человека, которого вы хотите найти в книге контактов:")

def get_data(tuser):
    tuser._getting_data = True
    bot.send_message(tuser.id, "Минутку, прогружаем книжку контактов...")

    all_data = db.get_data()
    tuser_data = all_data.get(str(tuser.id))
    if tuser_data:
        for user in tuser_data:
            user_data = f"{user["name"].capitalize()}\nНомер телефона: {user["phone_number"]}"
            if user["features"]: user_data += f"\nОтличительные черты: {", ".join(user["features"])}"
            bot.send_message(tuser.id, user_data)
            tuser._getting_data = False
    else:
        bot.send_message(tuser.id, "Ваша книжка пуста! Самое время добавить туда новых людей!")
        create_main_buttons(tuser.id)
        tuser._getting_data = False

bot.polling(none_stop=True)