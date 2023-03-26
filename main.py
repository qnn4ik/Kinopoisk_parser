import re
import os
import requests
from bs4 import BeautifulSoup
import json
from user_agent import generate_user_agent
from time import sleep
from random import randrange


def get_data(url):

    headers = {
    "accept": "*/*",
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru,en;q=0.9',
    'content-length': '193',
    'content-type': 'application/json',
    'cookie': 'yandex_login=; my_perpages=%5B%5D; mda_exp_enabled=1; _yasc=kLI4ArYYRdriADnar5aO1gzaUrh5yMu9uHfQzYv5LYEhzD2Kda8sXOtAW4Q=; ya_sess_id=noauth:1678779122; ys=c_chck.1351087663; i=xNElJjTi3+KwZJBDAMAt500dSaqOiFIGz3qriiqD4f6eo/VkDVtLssCZRezlKthY6G/6usgdk7OEGmilDQ6pKxP5w0E=; yandexuid=5329511351678714921; mda2_beacon=1678779122340; sso_status=sso.passport.yandex.ru:synchronized; location=1; crookie=8WQXr4cnykL3cIPz8FBNX3Y7AxLzQ/z8m79SgF9iL7c+5GjjGDRSY+TebN6juaSffWQtnweeJJscSpGTGvtivWlI67c=; cmtchd=MTY3ODc3OTYwNzIzOA==; coockoos=4',
    'user_Agent': generate_user_agent()
    }

    pages = 3

    for page in range(1, pages+1):
        print(f'#Страница {page}/{pages}')
        page_url = url + f'/?page={page}'
        req = requests.get(page_url, headers)

        if not os.path.isdir('data'):
            os.mkdir('data')

        with open(f'data/page_{page}.html', 'w', encoding='utf-8-sig') as file:
            file.write(req.text)

        with open(f'data/page_{page}.html', encoding='utf-8-sig') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        all_movies = soup.select('div[data-tid="8a6cbb06"] a[data-tid="d4e8d214"]')

        page_data = []

        for movie in all_movies:
            ru_title = movie.find('span', {'data-tid': "4502216a"}).text
            main_info = movie.find('span', {'data-tid': "31fba632"}).text.replace('\xa0', ' ').strip()
            director = movie.find('div', {'data-tid': "31fba632"}).find('span').text

            if 'Режиссёр:' in director:
                director = director.split('Режиссёр:')[-1].strip()
            main_roles = movie.find('span', text=re.compile('В ролях')).text.replace('В ролях: ', '')

            data = {
                'Название': ru_title,
                'Главная информация': main_info,
                'Режиссёр': director,
                'В ролях': main_roles,
            }

            page_data.append(data)

        with open(f"data/page_{page}.json", 'w', encoding='utf-8-sig') as file:
            json.dump(page_data, file, indent=4, ensure_ascii=False)

        sleep(randrange(3, 5))


def filter_pages(total=5):
    all_films = []
    all_films_filtered = []

    for page in range(1, total+1):
        page_data = {}
        try:
            with open(f'data/page_{page}.json', encoding='utf-8-sig') as file:
                page_data = json.load(file)
            all_films += page_data
        except Exception as e:
            print(e)

    all_films_filtered = filter(
        lambda movie: 'гарри' in movie.get("Название").lower(),
        all_films
    )

    for movie in all_films_filtered:
        print(movie)


def main():
    get_data('https://www.kinopoisk.ru/lists/movies/top250/')
    #filter_pages(3)


if __name__ == '__main__':
    main()