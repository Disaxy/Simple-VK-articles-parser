import argparse
import csv
import os
from time import sleep

from requests_html import HTML, Element, HTMLSession


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--group', dest='group', help='Группа вконтакте', type=str, default='@yvkurse')
    parser.add_argument(
        '--timeout', dest='timeout', help='Задержка в секундах', type=float, default=0.1)
    return parser.parse_args()


def get_html(url: str) -> HTML:
    session = HTMLSession()
    response = session.get(url)
    return response.html


def get_articles_links(url: str) -> set:
    html = get_html(url)
    article_count = int(html.find('.author_page_header__subscribers', first=True).text.split(
        'подписчиков')[-1].split(' ')[0])
    links = []
    count = 0

    while count < article_count:
        html = get_html(f'{url}?offset={count}')
        links += [block.absolute_links for block in html.find(
            '.author_page_block')]
        count += len(links)

    set_links = set()
    for link in links:
        set_links.update(link)

    return set_links


def get_articles(links: set, timeout: float) -> dict:
    articles = []

    def get_image_link(images: Element, article: dict, key: str) -> None:
        while len(images):
            img = images.pop()
            link = img.attrs.get('src')
            if link[-3:] == 'jpg':
                article.update({key: link})
                break

    for link in links:
        print(f'Парсим - {link}')
        try:
            html = get_html(link)
        except AttributeError:
            print('Упс... Пожалуйста увеличьте время задержки и перезапустите скрипт')
            break
        else:
            title = html.find('h1', first=True).text
            body = ''
            for p in html.find('p'):
                body += ' ' + p.text
            article = {
                'Заголовок': title,
                'Текст статьи': body
            }
            images = html.find('img')
            if images:
                get_image_link(images, article, 'ImageURL1')
            if len(images) > 1:
                get_image_link(images, article, 'ImageURL2')
            articles.append(article)
            sleep(timeout)

    return articles


def create_csv(csv_path: str, articles: dict) -> None:
    with open(csv_path, 'w') as file:
        writer = csv.DictWriter(file, delimiter=';', fieldnames=list(
            articles[0].keys()), quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for article in articles:
            writer.writerow(article)


if __name__ == '__main__':
    args = get_args()
    url = f'https://vk.com/{args.group}'
    print('Парсим ссылки на статьи...')
    links = get_articles_links(url)
    print('Найдено статей в группе:', url, ' - ', len(links))
    print('Парсим статьи...')
    articles = get_articles(links, args.timeout)
    print(f'Было спаршено - {len(articles)} статей')
    print('Сохраняем в csv...')
    csv_path = os.path.join(os.path.dirname(__file__),
                            f'articles-from-{args.group}.csv')
    create_csv(csv_path, articles)
    print(f'Ссылка на готовый csv - {os.path.abspath(csv_path)}')
