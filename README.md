# 🎮 Игровой проект на Pygame

## Описание

Коллекция мини-игр на Python с использованием Pygame:
- 🐍 **Змейка**
- 🔢 **2048**

В проекте реализовано:
- ✨ Анимированное меню и фон
- 🎵 Фоновая музыка и звуки кнопок
- 🔊 Регулировка громкости (ползунок с иконкой динамика)
- 🖥️ Адаптивный интерфейс
- 🖱️ Управление мышью и клавиатурой
- 📦 Сборка в `.exe` с помощью PyInstaller

---

## ООП в проекте

В коде используются основные принципы объектно-ориентированного программирования:

- **Класс `Button`**  
  Отвечает за кнопки интерфейса: хранит положение, текст, цвета, методы отрисовки, наведения и клика.  
  **Пример кода:**
  ```python
  class Button:
      def __init__(self, center_x_ratio, center_y_ratio, text, color, hover_color, dynamic_text=False):
          self.center_x_ratio = center_x_ratio
          self.center_y_ratio = center_y_ratio
          self.base_text = text
          self.color = color
          self.hover_color = hover_color
          self.is_hovered = False
          self.was_hovered = False
          self.dynamic_text = dynamic_text
          self.padding_x = scale_value(20, BASE_SCREEN_WIDTH, SCREEN_WIDTH)
          self.padding_y = scale_value(10, BASE_SCREEN_HEIGHT, SCREEN_HEIGHT)
          self.update_rect()
      
      def draw(self, surface):
          if self.dynamic_text:
              self.update_rect()
          color = self.hover_color if self.is_hovered else self.color
          pygame.draw.rect(surface, color, self.rect, border_radius=15)
          surface.blit(self.text_surf, self.text_rect)
  ```

- **Класс `Star`**  
  Описывает анимированные звёзды на фоне: координаты, скорость, методы обновления и отрисовки.  
  **Пример кода:**
  ```python
  class Star:
      def __init__(self):
          self.x = random.randint(0, SCREEN_WIDTH)
          self.y = random.randint(0, SCREEN_HEIGHT)
          self.size = random.randint(1, 3)
          self.speed = random.randint(1, 3)
      
      def update(self):
          self.y += self.speed
          if self.y > SCREEN_HEIGHT:
              self.y = 0
              self.x = random.randint(0, SCREEN_WIDTH)
      
      def draw(self, surface):
          pygame.draw.circle(surface, WHITE, (self.x, self.y), self.size)
  ```

- **Инкапсуляция**  
  Все свойства и методы классов логически сгруппированы, например, методы `update_rect` и `draw` в классе `Button` скрывают детали реализации.

- **Переиспользование**  
  Кнопки и звёзды создаются как объекты и используются во всех экранах (меню, играх, экране окончания).

---

## Установка зависимостей

Для запуска проекта необходим Python 3.7+.

Установите все зависимости одной командой:
```sh
pip install -r requirements.txt
```

Если файла `requirements.txt` нет, используйте:
```sh
pip install pygame numpy pyinstaller
```

---

## Запуск из исходников

1. **Положите звуковые файлы** (`background_music.wav`, `click.wav`, `button_hover.wav`) в папку с `main.py`.

2. **Запустите игру:**
    ```sh
    python main.py
    ```

---

## Сборка exe-файла

1. **Установите PyInstaller (если не установлен):**
    ```sh
    pip install pyinstaller
    ```

2. **Соберите exe с ресурсами и иконкой:**
    ```sh
    python -m pyinstaller --onefile --windowed --icon=icon.ico --add-data "background_music.wav;." --add-data "click.wav;." --add-data "button_hover.wav;." main.py
    ```
    - Готовый exe будет в папке `dist`.
    - Функция `resource_path` обеспечивает доступ к звуковым файлам в скомпилированном виде:  
      **Пример кода:**
      ```python
      def resource_path(relative_path):
          """Возвращает абсолютный путь к ресурсу, работает и для .exe и для .py"""
          if hasattr(sys, '_MEIPASS'):
              return os.path.join(sys._MEIPASS, relative_path)
          return os.path.join(os.path.abspath("."), relative_path)
      ```

---

## Управление

- **Меню:** мышь или клавиши 1, 2, 0
- **Змейка:** стрелки, P — пауза, ESC — назад
- **2048:** стрелки, R — рестарт, P — пауза, ESC — назад
- **Ползунок громкости:** мышью в правом верхнем углу

---

## Эмодзи в интерфейсе

- В меню и на ползунке громкости используется эмодзи 🔊 (динамик).
- Для корректного отображения эмодзи используется шрифт `Segoe UI Emoji`.  
  **Пример кода для ползунка громкости:**
  ```python
  def draw_volume_slider():
      slider_x = SCREEN_WIDTH - 160
      slider_y = 20
      slider_w = 120
      slider_h = 16
      pygame.draw.rect(screen, GRAY, (slider_x, slider_y, slider_w, slider_h), border_radius=8)
      pygame.draw.rect(screen, CYAN, (slider_x, slider_y, int(slider_w * volume), slider_h), border_radius=8)
      pygame.draw.rect(screen, WHITE, (slider_x, slider_y, slider_w, slider_h), 2, border_radius=8)
      emoji_font = pygame.font.SysFont('Segoe UI Emoji', scale_value(25, BASE_SCREEN_HEIGHT, SCREEN_HEIGHT))
      vol_icon = emoji_font.render("🔊", True, WHITE)
      icon_rect = vol_icon.get_rect()
      icon_rect.centery = slider_y + slider_h // 2
      icon_rect.right = slider_x - 8
      screen.blit(vol_icon, icon_rect)
  ```

---

## Авторы

- Ташевский
- Каравашкин
- Бехнуд
- Алексеев

---
