import redis
import config
# на серваке должно быть  bind 0.0.0.0 для того что бы все могли зайти по хосту ()
r=redis.StrictRedis(host='localhost', port=6379, db=0)

# Пытаемся узнать из базы «состояние» пользователя
def get_current_state(user_id):
        try:
            return r.get(user_id).decode('utf-8')
        except KeyError:  # Если такого ключа почему-то не оказалось
            return config.States.S_START.value  # значение по умолчанию - начало диалога

# Сохраняем текущее «состояние» пользователя в нашу базу
def set_state(user_id, value):
    try:
        r.set(user_id,value)

        return True
    except:
            # тут желательно как-то обработать ситуацию
        return False