# Simple-VK-articles-parser
Простой парсер статей из ВК

***

### Запуск
Парсер собирает все статьи в csv файл.
Делителем в файле является ";".

По умолчанию парсит группу https://vk.com/@yvkurse.
Можно парсить любую группу, для этого запустите скрипт с параметром
--group [Название групы] например: `python main.py --group @astronomy`
если вк ругается, необходимо увеличить задержку параметром --timeout [сек]
например: `python main.py --group @astronomy --timeout 1`

***

### Параметры
* --group [Название группы] - название группы для парсинга
* --timeout [Секунд] - задержка между статьями

***

### Установка
`git clone https://github.com/Disaxy/Simple-VK-articles-parser.git`  
`cd Simple-VK-articles-parser/`  
`pip install -r requirements.txt`
