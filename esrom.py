import sys
import os
import platform
import time  # Uyuma işlemleri için
import pygame  # Ses çalma için (pygame)
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QWidget, QFileDialog, QHBoxLayout, QAction, QMenuBar, QDialog, QVBoxLayout as QDialogLayout, QDialogButtonBox
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon
import numpy as np

# Harfleri Mors koduna çeviren sözlük
morse_code = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
    "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
    "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
    "Z": "--..", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
    "0": "-----"
}

# Mors kodundan harflere çeviren sözlük (tersi)
text_code = {v: k for k, v in morse_code.items()}


def convert_to_morse(text):
    """Metni Mors koduna çevirir."""
    text = text.upper()
    result = []
    for char in text:
        if char == " ":
            result.append(" / ")  # Kelime arası boşluk
        elif char in morse_code:
            result.append(morse_code[char])
    return " ".join(result)


def convert_to_text(morse):
    """Morse kodunu metne çevirir."""
    morse_chars = morse.split(" ")
    result = []
    for morse_char in morse_chars:
        if morse_char == "/":
            result.append(" ")  # Kelime arası boşluk
        elif morse_char in text_code:
            result.append(text_code[morse_char])
    return "".join(result)


def play_morse_sound(morse_code, speed=1):
    """Mors kodunu sesli olarak çalar (platforma göre farklı metodlar)."""
    pygame.mixer.init(frequency=22050, size=-16, channels=1)  # Ses özelliklerini başlat

    # Ses frekansı ve süreyi ayarlıyoruz
    dot_duration = 400 // speed  # Nokta için kısa süre
    dash_duration = 1000 // speed  # Tire için uzun süre
    gap_duration = 0.9 // speed  # Kısa boşluk
    word_gap_duration = 0.3 // speed  # Kelime boşluğu

    # Sesler için frekans
    beep_frequency = 300  # Hz cinsinden
    sample_rate = 10000  # Örnekleme oranı (Hz)

    def generate_tone(frequency, duration):
        """Bir ton sesi yaratır."""
        samples = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = 0.5 * np.sin(2 * np.pi * frequency * samples)  # Sine wave
        return np.array(wave * 32767, dtype=np.int16)  # Sesin int16 formatında olması gerekir

    for char in morse_code:
        if char == ".":
            sound_data = generate_tone(beep_frequency, dot_duration / 1000)  # Nokta
            beep_sound = pygame.mixer.Sound(sound_data)
            beep_sound.play(maxtime=dot_duration)
            pygame.time.wait(int(dot_duration))  # Burada bekleme süresi integer olmalı
        elif char == "-":
            sound_data = generate_tone(beep_frequency, dash_duration / 1000)  # Tire
            beep_sound = pygame.mixer.Sound(sound_data)
            beep_sound.play(maxtime=dash_duration)
            pygame.time.wait(int(dash_duration))  # Burada bekleme süresi integer olmalı
        elif char == " ":
            pygame.time.wait(int(word_gap_duration * 1000))  # Kelime boşluğu, saniye cinsinden milisaniyeye dönüştürülmeli
        pygame.time.wait(int(gap_duration * 1000))  # Karakterler arası kısa boşluk, saniyeden milisaniyeye dönüşüm yapılmalı


def get_logo_path():
    """Platforma göre doğru logo ve simge dosyasının yolunu döndürür."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "esromlo.png")
    elif platform.system() == "Linux" and os.path.exists("/usr/share/icons/hicolor/48x48/apps/esromlo.png"):
        return "/usr/share/icons/hicolor/48x48/apps/esromlo.png"
    elif platform.system() == "Darwin" and os.path.exists("/System/Library/Sounds/esromlo.png"):
        return "/System/Library/Sounds/esromlo.png"
    return "esromlo.png"  # Default logo

def get_icon_path():
    """Simge dosyasının yolunu döndürür."""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "esromlo.png")
    elif os.path.exists("/usr/share/icons/hicolor/48x48/apps/esromlo.png"):
        return "/usr/share/icons/hicolor/48x48/apps/esromlo.png"
    return None

LOGO_PATH = get_logo_path()
ICON_PATH = get_icon_path()


class MorseTranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ESROM")
        self.setFixedSize(550, 700)

        logo_path = get_logo_path()
        self.setWindowIcon(QIcon(logo_path))  # Uygulama simgesi olarak platforma özel logo dosyasını ekleyin
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Menü bar ekleme
        menubar = self.menuBar()
        help_menu = menubar.addMenu("...↓...")

        # Hakkında menü öğesi
        about_action = QAction("Hakkında!", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # Menü bar ve aksiyon metin rengini beyaz yapma
        menubar.setStyleSheet("QMenuBar { background-color: #242424; color: white; }"
                            "QMenu { background-color: #242424; color: white; }"
                            "QMenu::item { background-color: #242424; color: white; }"
                            "QMenu::item:selected { background-color: #4A90E2; color: white; }"
                            "QAction { color: white; }"
                            "QAction:hover { background-color: #4A90E2; }")

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Logo
        self.logo_label = QLabel()
        pixmap = QPixmap(get_logo_path())  # Platforma göre logo dosyasını yükle
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)
        
        
        # Başlık
        self.title_label = QLabel("ESROM")
        self.title_label.setFont(QFont("Helvetica Neue", 20, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: white;")  # Yazı rengini beyaz yap
        layout.addWidget(self.title_label)

        # Başlık
        self.title_label = QLabel(". ... .-. --- --")
        self.title_label.setFont(QFont("Helvetica Neue", 15, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: white;")  # Yazı rengini beyaz yap
        layout.addWidget(self.title_label)

        # Giriş Alanı
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Metin veya Morse kodu giriniz...")
        self.input_field.setStyleSheet("""
            background-color: #5A5A5A;
            color: white;
            padding: 15px;
            font-size: 18px;
            border-radius: 12px;
            border: none;
        """)
        self.input_field.setMaxLength(100)  # Maksimum uzunluk
        layout.addWidget(self.input_field)

        # Çeviri ve ses çalma seçenekleri
        buttons_layout = QHBoxLayout()
        self.translate_button = QPushButton("Çevir")
        self.translate_button.clicked.connect(self.translate)
        self.translate_button.setStyleSheet("""
            background-color: #4A90E2;
            color: white;
            padding: 12px;
            border-radius: 12px;
            border: none;
            font-size: 16px;
        """)
        buttons_layout.addWidget(self.translate_button)

        self.play_sound_button = QPushButton("Seslendir (BETA)")
        self.play_sound_button.clicked.connect(self.play_morse_sound)
        self.play_sound_button.setStyleSheet("""
            background-color: #4A90E2;
            color: white;
            padding: 12px;
            border-radius: 12px;
            border: none;
            font-size: 16px;
        """)
        buttons_layout.addWidget(self.play_sound_button)

        layout.addLayout(buttons_layout)


        # Çıktı Alanı
        self.output_label = QLabel()
        self.output_label.setWordWrap(True)
        self.output_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.output_label.setStyleSheet("""
            background-color: #342241;
            padding: 100px;
            border-radius: 12px;
            border: 1px solid #D3D3D3;
            color: white;
            font-size: 15px;  /* Daha büyük font boyutu */
            font-weight: bold;  /* Daha belirgin yazı */
        """)
        layout.addWidget(self.output_label)

        # Dosyaya kaydetme
        self.save_button = QPushButton("Dosyaya Kaydet")
        self.save_button.clicked.connect(self.save_to_file)
        self.save_button.setStyleSheet("""
            background-color: #4A90E2;
            color: white;
            padding: 12px;
            border-radius: 12px;
            border: none;
            font-size: 16px;
        """)
        layout.addWidget(self.save_button)

        # Merkezi widget
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Çıktıya tıklama ile kopyalama özelliği
        self.output_label.mousePressEvent = self.copy_output

        # Arka plan rengini ayarlama
        self.setStyleSheet("background-color: #242424;")

    def show_about(self):
        """Hakkında bilgisi gösterir."""
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("Hakkında")
        about_dialog.setFixedSize(400, 400)

        about_layout = QDialogLayout()

        about_text = QLabel("ESROM - Mors Kodu Çevirici Uygulaması\n\n"
                            "Bu uygulama, metin ve Mors kodu arasında dönüşüm yapmanızı sağlar. "
                            "Ayrıca Mors kodunu sesli olarak dinlemenize olanak tanır.\n\n"
                            " Geliştirici: ALG Yazılım Inc. | www.algyzilim.com | info@algyazilim.com\n\n"
                            " Fatih ÖNDER (CekToR) | wwww.fatihonder.org.tr | fatih@algyazilim.com\n\n"
                            " ESROM Tüm Hakları Saklıdır. 2024 ALG Software Inc\n\n"
                            " ALG Yazılım Pardus'a Göç'ü Destekler.\n\n"
                            " ESROM Sürüm: 1.0\n\n")

        about_text.setAlignment(Qt.AlignCenter)
        about_text.setWordWrap(True)  # Metnin kaydırılabilir olmasını sağlar
        about_text.setStyleSheet("color: white;")  # Hakkında bölümündeki metni beyaz yap
        about_layout.addWidget(about_text)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(about_dialog.accept)
        about_layout.addWidget(button_box)

        about_dialog.setLayout(about_layout)
        about_dialog.exec_()


    def translate(self):
        """Metni Mors koduna çevirir."""
        input_text = self.input_field.text().strip()
        if input_text:
            if all(char in ".- /" for char in input_text):  # Morse kodu girişi
                self.output_label.setText(convert_to_text(input_text))
            else:  # Metin girişi
                self.output_label.setText(convert_to_morse(input_text))

    def play_morse_sound(self):
        """Mors kodunu sesli olarak çalar."""
        input_text = self.input_field.text().strip()
        if input_text:
            if all(char in ".- /" for char in input_text):  # Morse kodu girişi
                play_morse_sound(input_text)
            else:  # Metin girişi
                morse = convert_to_morse(input_text)
                play_morse_sound(morse)

    def save_to_file(self):
        """Çıktıyı bir dosyaya kaydeder."""
        file_dialog = QFileDialog(self)
        file_dialog.setDefaultSuffix(".txt")
        file_path, _ = file_dialog.getSaveFileName(self, "Kaydet", "", "Metin Dosyası (*.txt)")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.output_label.text())

    def copy_output(self, event):
        """Çıktıyı panoya kopyalar."""
        output_text = self.output_label.text()

        clipboard = QApplication.clipboard()
        clipboard.setText(self.output_label.text())
        
        # "Kopyalandı" mesajını göster
        self.output_label.setText(f"Kopyalandı: {output_text}")
        
        # 2 saniye sonra "Kopyalandı" mesajını sil
        QTimer.singleShot(1000, lambda: self.output_label.setText(output_text))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    if ICON_PATH:
        app.setWindowIcon(QIcon(ICON_PATH))
    window = MorseTranslatorApp()
    window.show()
    sys.exit(app.exec_())
