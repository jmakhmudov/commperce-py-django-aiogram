def mute_restrict_text(admin, member, mute_time, attribute, comment):
    term = None
    variables = {
        "s": {1: "секунда", 2: "секунды", 3: "секунд"},
        "m": {1: "минута", 2: "минуты", 3: "минут"},
        "h": {1: "час", 2: "часа", 3: "часов"},
        "d": {1: "день", 2: "дня", 3: "дней"},
        "w": {1: "неделя", 2: "недели", 3: "недель"},
    }
    if comment is None:
        comment = "Не указана"
    if mute_time == 1:
        term = variables[attribute][1]
    elif 1 < mute_time < 5:
        term = variables[attribute][2]
    elif mute_time >= 5:
        term = variables[attribute][3]
    return f"""
{admin} запретил отправлять сообщения участнику чата {member}
Срок: {mute_time} {term}
Причина: {comment}
"""


def unmute_restrict_text(member):
    return f"""
{member} снова может отправлять сообщения!    
"""
