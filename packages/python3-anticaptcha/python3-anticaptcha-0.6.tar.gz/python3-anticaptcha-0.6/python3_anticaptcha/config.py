# Адрес для создания задачи
create_task_url = "https://api.anti-captcha.com/createTask"
# Адрес для получения ответа
get_result_url = "https://api.anti-captcha.com/getTaskResult"
# Адрес для получения баланса
get_balance_url = "https://api.anti-captcha.com/getBalance"
# Адрес для отправки жалобы на неверное решение капчи
incorrect_captcha_url = "https://api.anti-captcha.com/reportIncorrectImageCaptcha"
# Адрес для получения информации об очереди
get_queue_status_url = "https://api.anti-captcha.com/getQueueStats"
# ключ приложения
app_key = "1899"
# random user agent data
# получаем рандомный userAgent
from fake_useragent import UserAgent

user_agent_data = UserAgent(cache=False).random


# todo Удалить это всё
TEST_KEY = 'ae23fffcfaa29b170e3843e3a486ef19'


# для тестирования ReCaptcha
websiteURL='https://www.google.com/recaptcha/intro/android.html'
websiteKey='6LeuMjIUAAAAAODtAglF13UiJys0y05EjZugej6b'

