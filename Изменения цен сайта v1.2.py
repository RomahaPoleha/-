import os
import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class MainPage:
    def __init__(self, path_to_site):
        self.path_to_site = path_to_site

    def replace_price_in_line(self, name_file, line_number, new_price):
        full_path = os.path.join(self.path_to_site, name_file)

        with open(full_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        line = lines[line_number]

        modified_line = re.sub(
            r'(<div class="price">)\s*[\d\s]+(\s*руб\.?\s*</div>)',
            rf'\g<1>{new_price}\g<2>',
            line
        )

        lines[line_number] = modified_line

        with open(full_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)


class PriceInputPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Введите цены для интерактивных досок New Touch kids'
        self.size_hint = (0.8, 0.8)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Первая цена
        layout.add_widget(Label(text='Цена основной страницы(Так-е будут изменены соответствующие цены с дополнительной таблицы):'))
        self.price1_input = TextInput(multiline=False)
        layout.add_widget(self.price1_input)

        # Вторая цена
        layout.add_widget(Label(text='Цена дополнительной страницы инт.доска с ноутбуком:'))
        self.price2_input = TextInput(multiline=False)
        layout.add_widget(self.price2_input)

        # Третья цена
        layout.add_widget(Label(text='Цена с ноутбуком и колонками:'))
        self.price3_input = TextInput(multiline=False)
        layout.add_widget(self.price3_input)

        # Кнопка подтверждения
        submit_btn = Button(text='Применить', size_hint_y=0.2)
        submit_btn.bind(on_press=self.apply_prices)
        layout.add_widget(submit_btn)

        self.content = layout

        # Инициализация путей к файлам
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path_to_public_html = os.path.join(current_dir, 'public_html')
        path_to_public_html_kids = os.path.join(current_dir, 'public_html', 'products')

        self.main_page = MainPage(path_to_public_html)
        self.additional_page = MainPage(path_to_public_html_kids)

    def validate_price(self, price):
        return re.match(r'^[\d\s]+$', price) is not None

    def apply_prices(self, instance):
        price1 = self.price1_input.text
        price2 = self.price2_input.text
        price3 = self.price3_input.text

        if not all(self.validate_price(p) for p in [price1, price2, price3]):
            error_popup = Popup(title='Ошибка',
                                content=Label(text='Введите только цифры и пробелы!'),
                                size_hint=(0.6, 0.4))
            error_popup.open()
            return

        # Применяем первую цену
        self.main_page.replace_price_in_line("index.php", 368, price1)
        self.additional_page.replace_price_in_line("kids.html", 290, price1)
        self.additional_page.replace_price_in_line("kids.html", 767, price1)

        # Применяем вторую цену
        self.additional_page.replace_price_in_line("kids.html", 302, price2)
        self.additional_page.replace_price_in_line("kids.html", 779, price2)

        # Применяем третью цену
        self.additional_page.replace_price_in_line("kids.html", 314, price3)
        self.additional_page.replace_price_in_line("kids.html", 791, price3)

        self.dismiss()
        success_popup = Popup(title='Успех',
                              content=Label(text='Цены успешно изменены!'),
                              size_hint=(0.6, 0.4))
        success_popup.open()


class MainApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        btn = Button(text='New Touch', size_hint=(0.5, 0.2),
                     pos_hint={'center_x': 0.5})
        btn.bind(on_press=self.show_price_popup)

        layout.add_widget(btn)
        return layout

    def show_price_popup(self, instance):
        popup = PriceInputPopup()
        popup.open()


if __name__ == '__main__':
    MainApp().run()