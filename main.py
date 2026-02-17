import sys
import json
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QProgressBar, QCheckBox, QMessageBox, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class TermsTrainer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.terms = []
        self.current_term = None
        self.learned_count = 0
        self.hard_terms_ids = [] 
        
        self.init_ui()
        self.load_data()
        self.apply_styles()
        self.next_term()

    def init_ui(self):
        self.setWindowTitle("Тренажёр терминов по программированию")
        self.setMinimumSize(600, 500)
        self.setStyleSheet("background-color: #2b2b2b; color: #ffffff;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        top_layout = QHBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #555;
                border-radius: 5px;
                text-align: center;
                background-color: #444;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)
        self.progress_label = QLabel("Изучено: 0 из 0")
        self.progress_label.setStyleSheet("font-weight: bold; color: #aaa;")
        
        progress_container = QVBoxLayout()
        progress_container.addWidget(self.progress_label)
        progress_container.addWidget(self.progress_bar)
        top_layout.addLayout(progress_container, stretch=2)

        filters_layout = QVBoxLayout()
        
        self.category_combo = QComboBox()
        self.category_combo.addItem("Все категории")
        self.category_combo.currentIndexChanged.connect(self.next_term)
        
        self.hard_mode_check = QCheckBox("Только сложные")
        self.hard_mode_check.stateChanged.connect(self.next_term)
        self.hard_mode_check.setStyleSheet("QCheckBox { color: #ff6b6b; font-weight: bold; }")

        filters_layout.addWidget(self.category_combo)
        filters_layout.addWidget(self.hard_mode_check)
        top_layout.addLayout(filters_layout, stretch=1)

        main_layout.addLayout(top_layout)

        card_frame = QFrame()
        card_frame.setStyleSheet("""
            QFrame {
                background-color: #3c3f41;
                border-radius: 10px;
                border: 1px solid #555;
            }
        """)
        card_layout = QVBoxLayout(card_frame)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setAlignment(Qt.AlignCenter)

        self.term_label = QLabel("Термин")
        self.term_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.term_label.setAlignment(Qt.AlignCenter)
        self.term_label.setStyleSheet("color: #64b5f6; margin-bottom: 10px;")

        self.definition_label = QLabel("Нажмите 'Показать определение', чтобы увидеть ответ")
        self.definition_label.setFont(QFont("Arial", 14))
        self.definition_label.setAlignment(Qt.AlignCenter)
        self.definition_label.setWordWrap(True)
        self.definition_label.setStyleSheet("color: #e0e0e0; min-height: 60px;")
        self.definition_label.hide()

        card_layout.addWidget(self.term_label)
        card_layout.addWidget(self.definition_label)
        main_layout.addWidget(card_frame, stretch=1)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_show = QPushButton("Показать определение")
        self.btn_show.clicked.connect(self.show_definition)
        self.btn_show.setStyleSheet(self.get_btn_style("#FFC107", "#000"))

        self.btn_dont_know = QPushButton("Не знаю")
        self.btn_dont_know.clicked.connect(self.mark_hard)
        self.btn_dont_know.setStyleSheet(self.get_btn_style("#FF5252", "#fff"))

        self.btn_know = QPushButton("Знаю")
        self.btn_know.clicked.connect(self.mark_learned)
        self.btn_know.setStyleSheet(self.get_btn_style("#4CAF50", "#fff"))

        self.btn_random = QPushButton("Случайный термин")
        self.btn_random.clicked.connect(self.next_term)
        self.btn_random.setStyleSheet(self.get_btn_style("#2196F3", "#fff"))

        self.btn_dont_know.hide()
        self.btn_know.hide()

        btn_layout.addWidget(self.btn_show)
        btn_layout.addWidget(self.btn_dont_know)
        btn_layout.addWidget(self.btn_know)
        btn_layout.addWidget(self.btn_random)

        main_layout.addLayout(btn_layout)

    def get_btn_style(self, bg_color, text_color):
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: {text_color};
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: lighten({bg_color}, 10%);
                opacity: 0.9;
            }}
            QPushButton:pressed {{
                background-color: darken({bg_color}, 10%);
            }}
        """

    def apply_styles(self):
        pass

    def load_data(self):
        try:
            with open('terms.json', 'r', encoding='utf-8') as f:
                self.terms = json.load(f)
            
            for term in self.terms:
                if 'is_learned' not in term:
                    term['is_learned'] = False
                if 'is_hard' not in term:
                    term['is_hard'] = False
            
            self.update_progress()
            self.populate_categories()
            
        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "Файл terms.json не найден!")
            sys.exit()
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Ошибка", "Ошибка чтения JSON файла!")
            sys.exit()

    def save_data(self):
        try:
            with open('terms.json', 'w', encoding='utf-8') as f:
                json.dump(self.terms, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def populate_categories(self):
        categories = set(term['category'] for term in self.terms)
        for cat in sorted(categories):
            self.category_combo.addItem(cat)

    def get_filtered_terms(self):
        category = self.category_combo.currentText()
        is_hard_mode = self.hard_mode_check.isChecked()
        filtered = self.terms
        
        if category != "Все категории":
            filtered = [t for t in filtered if t['category'] == category]
            
        if is_hard_mode:
            filtered = [t for t in filtered if t.get('is_hard', False) and not t.get('is_learned', False)]
            if not filtered:
                QMessageBox.information(self, "Инфо", "Нет сложных терминов в этой категории для повторения!")
                self.hard_mode_check.setChecked(False)
                return self.get_filtered_terms()
        else:
            filtered = [t for t in filtered if not t.get('is_learned', False)]

        return filtered

    def next_term(self):
        self.definition_label.hide()
        self.btn_show.show()
        self.btn_dont_know.hide()
        self.btn_know.hide()
        
        available_terms = self.get_filtered_terms()
        
        if not available_terms:
            self.term_label.setText("Поздравляем!")
            self.definition_label.setText("Все термины в выбранной категории изучены.")
            self.definition_label.show()
            self.btn_show.hide()
            return

        self.current_term = random.choice(available_terms)
        self.term_label.setText(self.current_term['term'])
        self.definition_label.setText(self.current_term['definition'])

    def show_definition(self):
        self.definition_label.show()
        self.btn_show.hide()
        self.btn_dont_know.show()
        self.btn_know.show()

    def mark_learned(self):
        if self.current_term:
            self.current_term['is_learned'] = True
            self.current_term['is_hard'] = False 
            self.save_data()
            self.update_progress()
            self.next_term()

    def mark_hard(self):
        if self.current_term:
            self.current_term['is_hard'] = True
            self.save_data()
            self.update_progress()
            self.next_term()

    def update_progress(self):
        total = len(self.terms)
        learned = sum(1 for t in self.terms if t.get('is_learned', False))
        self.progress_label.setText(f"Изучено: {learned} из {total}")
        percentage = int((learned / total) * 100) if total > 0 else 0
        self.progress_bar.setValue(percentage)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = TermsTrainer()
    window.show()
    sys.exit(app.exec_())