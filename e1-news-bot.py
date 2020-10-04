# TODO
# 1. $$('div[class*="video"]') если в статье есть видео, нужно передавать ссылку на видео
# 2. Оторбажение фоток
# 3. Красивое форматирование текста
# 4. Логирование
# 5. Отслеживание ошибок
# 6. Болле точная проверка появления новых новостей


import requests
from bs4 import BeautifulSoup
import time
import telebot

base_url = "https://www.e1.ru"
post_link = ""

TOKEN = '1289644176:AAG4yRgFOEHYCwabDmQpxhPqIRNcXslh6Js'
CHANNEL_NAME = '@e1_unofficial'
TIME_TO_CHECK_NEWS = 300

bot = telebot.TeleBot(TOKEN)


def send_new_post(new_post):
    bot.send_message(chat_id=CHANNEL_NAME, text=new_post)


def get_soup(link):
    try:
        req = requests.get(link).text
        return BeautifulSoup(req, 'html.parser')
    except requests.ConnectionError:
        print("Error")
        time.sleep(10)
        get_soup(link)



def get_first_post_link(soup):
    first_news = soup.find_all("h2")[1]  # Первая новость
    return first_news.find("a")["href"]


def contains_waste_words(text):
    waste_words = ["Поделиться", " Поделиться", "Фото: ", "У нас есть почтовая рассылка", "Пока нет ни одного комментария"]
    for word in waste_words:
        if text.startswith(word):
            return True
    return False


def get_news_text(soup, link):
    all_p = soup.find_all("p")  # Все абзацы новости
    news_header = soup.find_all("h2")[1].get_text()  # Заголовок новости
    news_paragraphs = ''
    for p in all_p:
        paragraph = p.get_text()
        if not contains_waste_words(paragraph):
            news_paragraphs += " \r\n " + p.get_text()

    print(news_header + news_paragraphs + ' Эта же новость на e1.ru: ' + link)
    return news_header + news_paragraphs + ' Эта же новость на e1.ru: ' + link


if __name__ == "__main__":
    while True:
        soup = get_soup(base_url + "/news/")
        post_time = soup.find("time").text
        new_post_link = get_first_post_link(soup)
        if post_link != new_post_link:
            post_link = new_post_link
            soup = get_soup(base_url + new_post_link)
            message = get_news_text(soup, base_url + new_post_link)
            send_new_post(message)
        else:
            print("new post hasn't found")
        time.sleep(TIME_TO_CHECK_NEWS)
