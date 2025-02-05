DOMAIN = "emaktab"
CONF_USERNAME = "username" #логин
CONF_PASSWORD = "password" #пароль
CONF_CAPTCHA = "639dcede-f3e1-4e2f-8ef2-17f5f53aaca6" #Идентификатор каптчи. произвольный UUID
CONF_PERSON_ID = "person_id" #Идентификатор ученика, например: 1000009940640
CONF_SCHOOL_ID = "school_id" #Идентификатор школы, например: 1000000000108
CONF_GROUP_ID = "group_id" #Идентификатор группы учащихся, например: 2248292570190413489
CONF_TAKEDAYS = 1 #Количество дней расписания
UPDATE_INTERVAL = 3600  # Обновление раз в час
BASE_URL = "https://emaktab.uz"
LOGIN_URL = "https://login.emaktab.uz/"
SCHEDULE_URL = BASE_URL + "/api/userfeed/persons/{}/schools/{}/groups/{}/schedule?date={}&takeDays=" + CONF_TAKEDAYS
