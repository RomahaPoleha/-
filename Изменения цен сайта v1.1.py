import os
import re

class MainPage:
    def __init__(self, path_to_site):
        self.path_to_site = path_to_site

    def replace_price_in_line(self, name_file, line_number, new_price):
        full_path = os.path.join(self.path_to_site, name_file)

        with open(full_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        line = lines[line_number]

        modified_line = re.sub(
            r'(<div class="price">)\s*[\d\s]+(\s*руб\.?\s*</div>)',  # учтёт "руб." и "руб"
            rf'\g<1>{new_price}\g<2>',
            line
        )

        lines[line_number] = modified_line

        with open(full_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)

def get_valid_price(prompt):
    while True:
        price = input(prompt)
        if re.match(r'^[\d\s]+$', price):
            return price
        print("Ошибка: введите только цифры и пробелы (например: '100 000')")

# Автоматическое определение пути к файлу index.php
current_dir = os.path.dirname(os.path.abspath(__file__))
path_to_public_html = os.path.join(current_dir,  'public_html')

# Автоматическое определение пути к файлу kids.html
current_dir2 = os.path.dirname(os.path.abspath(__file__))
path_to_public_html_kids = os.path.join(current_dir2,  'public_html', 'products')
# Создаём объект
main_page = MainPage(path_to_public_html)
additional_page = MainPage(path_to_public_html_kids)

def mainpage_interactive_whiteboards():
    # Меняем цену основной страницы сайта раздела "Интерактивных досок"
    new_price = get_valid_price("Введите цену основной страницы сайта для New Touch Kids")
    main_page.replace_price_in_line("index.php", 368, new_price)
    additional_page.replace_price_in_line("kids.html", 290, new_price)
    additional_page.replace_price_in_line("kids.html", 767, new_price)


mainpage_interactive_whiteboards()

def additional_page_interactive_whiteboards():
    # Меняем цену дополнительной страницы "Интерактивных досок"
    new_price = get_valid_price("Введите цену основной страницы сайта New Touch Kids(Комплектация с ноутбуком)")
    additional_page.replace_price_in_line("kids.html", 302, new_price)
    additional_page.replace_price_in_line("kids.html", 779, new_price)

    new_price2=get_valid_price("Введите цену основной страницы сайта New Touch Kids(Комплектация с ноутбуком и аудиоколонками)")
    additional_page.replace_price_in_line("kids.html", 314, new_price2)
    additional_page.replace_price_in_line("kids.html", 791, new_price2)

additional_page_interactive_whiteboards()