# beshparmak_locker.py
import tkinter as tk
from tkinter import messagebox
import pygame
import os
import sys

PASSWORD = "1234"
TIME_LIMIT = 3 * 3600  # 3 часа
MUSIC_FILE = "music.mp3"  # имя файла в той же папке


class BeshparmakLocker:
    def __init__(self):
        # Инициализируем pygame для музыки
        pygame.mixer.init()

        self.root = tk.Tk()
        self.root.title("БЕШПАРМАК СИСТЕМАСЫ")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#00008B')
        self.root.resizable(False, False)

        self.root.protocol("WM_DELETE_WINDOW", lambda: None)
        self.root.bind('<Escape>', lambda e: None)

        self.time_left = TIME_LIMIT
        self.music_started = False

        self.init_ui()
        self.start_music()  # Запускаем музыку
        self.update_timer()

        self.root.mainloop()

    def start_music(self):
        """Запускает MP3 в бесконечном цикле"""
        try:
            # Проверяем существует ли файл
            if getattr(sys, 'frozen', False):
                # Если запущено как .exe
                base_path = sys._MEIPASS
            else:
                # Если запущено как .py
                base_path = os.path.dirname(os.path.abspath(__file__))

            music_path = os.path.join(base_path, MUSIC_FILE)

            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)  # -1 = бесконечный повтор
                self.music_started = True
            else:
                print(f"Файл {MUSIC_FILE} не найден в {base_path}")
        except Exception as e:
            print(f"Ошибка воспроизведения: {e}")

    def stop_music(self):
        """Останавливает музыку"""
        if self.music_started:
            pygame.mixer.music.stop()

    def init_ui(self):
        # ГЛАВНЫЙ ЗАГОЛОВОК
        header_frame = tk.Frame(self.root, bg='#00008B')
        header_frame.pack(fill=tk.X, pady=(20, 0))

        self.warning_label = tk.Label(
            header_frame,
            text="БЕШПАРМАК ЗАБЛОКИРОВАЛ СИСТЕМУ",
            font=("Consolas", 36, "bold"),
            fg="#FF4444",
            bg='#00008B'
        )
        self.warning_label.pack()

        self.sub_label = tk.Label(
            header_frame,
            text="ОТДАЙ БЕШПАРМАК ИЛИ ВВЕДИ ПАРОЛЬ",
            font=("Consolas", 14, "bold"),
            fg="#FFAA00",
            bg='#00008B'
        )
        self.sub_label.pack(pady=(10, 5))

        separator = tk.Label(
            header_frame,
            text="=" * 80,
            font=("Consolas", 12),
            fg="white",
            bg='#00008B'
        )
        separator.pack(pady=(10, 20))

        main_frame = tk.Frame(self.root, bg='#00008B')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Левая панель
        left_frame = tk.Frame(main_frame, bg='#00008B', width=800)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.by_label = tk.Label(
            left_frame,
            text="by melorazm | БЕШПАРМАК СИЛА",
            font=("Consolas", 14),
            fg="#FFAA00",
            bg='#00008B'
        )
        self.by_label.pack(pady=(20, 10))

        # ASCII-арт (ваша маска)
        ascii_art = r"""
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::...
..-@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:..
..-@@#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++%@@:..
..-@@* ............................................................#@@:..
..-@@* .-%%%%%%%%%%%%%%%%%%%%%##*++====++*##%%%%%%%%%%%%%%%%%%%%:..#@@:..
..-@@* .-@@@@@@@@@@@@@%*=::.....          .....:-+#%@@@@@@@@@@@%:..#@@:..
..-@@* .-@@@@@@@@@#=:....                         ..:-*%@@@@@@@%:..#@@:..
..-@@* .-@@@@@%#=:..                                 ...-*%@@@@%:..#@@:..
..-@@* .-@@@%+:.                                         .:+%@@%:..#@@:..
..-@@* .-@%*:.                                             .:*%%:..#@@:..
..-@@* .-%=.                                                 .=%:..#@@:..
..-@@* .:-.                                                    -...#@@:..
..-@@* ...                                                        .#@@:..
..-@@* ....                                                   ... .#@@:..
..-@@* .-@%*:.    ....::...                  ....::...     .:*%#. .#@@:..
..-@@* .-@@@#....=*%@@@@@@%#=:.           .:=#%@@@@@%%*=.. :#@@#. .#@@:..
..-@@*...+#%%-:*%%#+-:-+%@@@@%*-.      ..-*%@@@@%+-:-+#@%*::%@#-...#@@:..
..-@@* .-@@@%==*=..    ..=#@@@@@%*-. .=#%@@@@@#=..    .:=*=+%@@%. .#@@:..
..-@@* .:+#%@#. ..       ..-#%@@@@*: :*@@@@%#-..      ... .#%*+-. .#@@:..
..-@@* .-%@#+...::.   .......:+%%*-. .-#%%+:........  .::...+#@#. .#@@:..
..-@@* .-+.. .:#+.....=#%%%+:.......   .....-*%%%#-... .**:...:+. .#@@:..
..-@@* ..... .+%: .:*@@@@@@@@#-. .........-#@@@@@@@@+:..=%-.  ... .#@@:..
..-@@*       .:#:..=@@@@@@@@@@*:.:+-..+=.-#@@@@@@@@@@-..=+:.      .#@@:..
..-@@*       ....-*#*+===*#@%+...-*- .++..:+%%#+===+##*:...       .#@@:..
..-@@*         ..-:..    ..:-+-.:+*: .=*-.-+-...   ...::..        .#@@:..
..-@@*       ..:-..         ..:+*=..  .:+*=..         ..-...      .#@@:..
..-@@*     ..:*%=.          .-*=..      .:*+.          .=#+:..    .#@@:..
..-@@*   ...=@@#.           .=*:         .=+:           :#@%=..   .#@@:..
..-@@*   ..*@@@#.        ...:-==:..   ..-++=:....      .:#@@@+..  .#@@:..
..-@@*   .=@@@@%+..   ..:+%@@@@@@*.. .=%@@@@@@%+:..   ..*%@@@@-.  .#@@:..
..-@@*  ..*@@@@@@%%%%%%%@@@@@@@@@@%%%%@@@@@@@@@@@%%##%%%@@@@@@-.  .#@@:..
..-@@*   .+@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%:.  .#@@:..
..-@@* .-=:#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=.=...#@@:..
..-@@* .-%*-#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%=:*%:..#@@:..
..-@@* .-@@#::+*%%@@@@@@@@%%%#*#@@@@@@@@%#*#%@@@@@@@@@%%#*+::#@@:..#@@:..
..-@@* .-@@@%:.  .......-*%%%%*==+++======*%@%%#=.......  .:#@@@:..#@@:..
..-@@* .-@@@@#.         .:#@@@@@@@@@@@@@@@@@@@%=.         .*@@@@:..#@@:..
..-@@* .-@@@@%-.          .-#@@@@@@@@@@@@@@@%=..         .-%@@@@:..#@@:..
..-@@* .-@@@@%=            ...:+%@@@@@@@#=:...           .*@@@@@:..#@@:..
..-@@* .-@@@@@*.              .............              .#@@@@@:..#@@:..
..-@@* .-@@@@@%-.                                       .=%@@@@@:..#@@:..
..-@@* .-@@@@@@#:.                                     .:#@@@@@@:..#@@:..
..-@@* .-@@@@@@@%-..                                  .:#@@@@@@@:..#@@:..
..-@@* .-@@@@@@@@%+..                               ..=%@@@@@@@@:..#@@:..
..-@@* .-@@@@@@@@@@#-.                            ..-#@@@@@@@@@@:..#@@:..
..-@@* .-@@@@@@@@@@@@#-.                        ..=#@@@@@@@@@@@@:..#@@:..
..-@@* .-@@@@@@@@@@@@@@#-.                     .=%@@@@@@@@@@@@@@:..#@@:..
..-@@* ...................                     ....................#@@:..
..-@@*:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::%@@:..
..-@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:..
..:-------------------------------------------------------------------...
"""
        self.ascii_label = tk.Label(
            left_frame,
            text=ascii_art,
            font=("Consolas", 10),
            fg="white",
            bg='#00008B',
            justify=tk.LEFT
        )
        self.ascii_label.pack(pady=10)

        # КАТАКБАС СИЛА (добавлено)
        self.beshparmak_label = tk.Label(
            left_frame,
            text="КАТАКБАС СИЛА",
            font=("Consolas", 24, "bold"),
            fg="#FFAA00",
            bg='#00008B'
        )
        self.beshparmak_label.pack(pady=(10, 5))

        # Таймер
        self.timer_label = tk.Label(
            left_frame,
            text=self.format_time(self.time_left),
            font=("Consolas", 48, "bold"),
            fg="white",
            bg='#00008B'
        )
        self.timer_label.pack(pady=(20, 40))

        # Правая панель
        right_frame = tk.Frame(main_frame, bg='#00008B', width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        spacer_top = tk.Frame(right_frame, bg='#00008B', height=200)
        spacer_top.pack()

        self.prompt_label = tk.Label(
            right_frame,
            text="ВВЕДИТЕ ПАРОЛЬ:",
            font=("Consolas", 20, "bold"),
            fg="white",
            bg='#00008B'
        )
        self.prompt_label.pack()

        self.entry = tk.Entry(
            right_frame,
            font=("Consolas", 18),
            show="*",
            width=25,
            bg='black',
            fg='white',
            insertbackground='white'
        )
        self.entry.pack(pady=20)
        self.entry.focus_set()
        self.entry.bind('<Return>', lambda e: self.check_password())

        self.btn = tk.Button(
            right_frame,
            text="РАЗБЛОКИРОВАТЬ",
            font=("Consolas", 14, "bold"),
            command=self.check_password,
            bg='#444444',
            fg='white',
            activebackground='#666666',
            activeforeground='white'
        )
        self.btn.pack(pady=10)

    def format_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=self.format_time(self.time_left))
            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="00:00:00")
            self.entry.config(state='disabled')
            self.btn.config(state='disabled')
            self.stop_music()
            messagebox.showerror("ВРЕМЯ ВЫШЛО", "НЕТ ИДИ НАХУЙ, БЕШПАРМАК СЪЕЛ ТВОЮ ВИНДУ")

    def check_password(self):
        if self.entry.get() == PASSWORD:
            self.stop_music()
            self.root.destroy()
        else:
            messagebox.showerror("ОШИБКА", "НЕТ ИДИ НАХУЙ")
            self.entry.delete(0, tk.END)


if __name__ == "__main__":
    app = BeshparmakLocker()