import sys
import requests
from io import BytesIO
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, 
                             QLineEdit, QSlider, QCheckBox, QTextEdit, QHBoxLayout, QMessageBox, QGridLayout, QRadioButton)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import os

class DiaryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Funky Virtual Diary")
        self.setGeometry(100, 100, 1200, 700)

        # Load background image from URL
        self.load_background_image("https://i.postimg.cc/0jtwKScH/Untitled-design-15.jpg")

        # Central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Left frame
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(left_widget, stretch=4)

        # Right frame
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(right_widget, stretch=4)

        # Center frame (for quote)
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        main_layout.addWidget(center_widget, stretch=2)

        # --- Date Section ---
        date_label = QLabel(f"Date: {datetime.now().strftime('%Y-%m-%d')}", self)
        date_label.setStyleSheet("font: bold 12pt 'Comic Sans MS'; color: #8B0000;")
        left_layout.addWidget(date_label)

        # --- Today's Reflection Section ---
        reflection_label = QLabel("Today's Reflection", self)
        reflection_label.setStyleSheet("font: bold 14pt 'Comic Sans MS'; color: #8B0000;")
        left_layout.addWidget(reflection_label)

        # Happiness Score
        happiness_label = QLabel("Happiness Score (1-5)", self)
        happiness_label.setStyleSheet("font: bold 10pt 'Comic Sans MS'; color: #006400;")
        self.happiness_slider = QSlider(Qt.Orientation.Horizontal)
        self.happiness_slider.setRange(1, 5)
        self.happiness_slider.setValue(1)
        self.happiness_slider.setMaximumWidth(150)
        happiness_hbox = QHBoxLayout()
        happiness_hbox.addWidget(happiness_label)
        happiness_hbox.addWidget(self.happiness_slider)
        left_layout.addLayout(happiness_hbox)

        # Productivity Score
        productivity_label = QLabel("Productivity Score (1-5)", self)
        productivity_label.setStyleSheet("font: bold 10pt 'Comic Sans MS'; color: #006400;")
        self.productivity_slider = QSlider(Qt.Orientation.Horizontal)
        self.productivity_slider.setRange(1, 5)
        self.productivity_slider.setValue(1)
        self.productivity_slider.setMaximumWidth(150)
        productivity_hbox = QHBoxLayout()
        productivity_hbox.addWidget(productivity_label)
        productivity_hbox.addWidget(self.productivity_slider)
        left_layout.addLayout(productivity_hbox)

        # Reduce space before Unhappy Moment Section
        left_layout.addSpacing(-5)

        # Unhappy Moment Section
        unhappy_reason_label = QLabel("Reason for Unhappy Moment", self)
        unhappy_reason_label.setStyleSheet("font: bold 10pt 'Comic Sans MS'; color: #006400;")
        self.unhappy_reason_entry = QTextEdit(self)
        self.unhappy_reason_entry.setMaximumHeight(100)
        self.unhappy_reason_entry.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #006666; background-color: rgba(255, 255, 255, 0.8);")
        unhappy_importance_label = QLabel("Importance of Unhappy Reason", self)
        unhappy_importance_label.setStyleSheet("font: bold 10pt 'Comic Sans MS'; color: #006400;")

        # Radio buttons for importance
        self.importance_group = QVBoxLayout()
        self.radio_important = QRadioButton("Important", self)
        self.radio_not_important = QRadioButton("Not Important", self)
        self.radio_should_not_care = QRadioButton("Should Not Care", self)
        self.radio_important.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #800080;")
        self.radio_not_important.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #800080;")
        self.radio_should_not_care.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #800080;")
        self.radio_important.setChecked(True)  # Default selection
        self.importance_group.addWidget(self.radio_important)
        self.importance_group.addWidget(self.radio_not_important)
        self.importance_group.addWidget(self.radio_should_not_care)

        unhappy_grid = QGridLayout()
        unhappy_grid.addWidget(unhappy_reason_label, 0, 0)
        unhappy_grid.addWidget(self.unhappy_reason_entry, 1, 0)
        unhappy_grid.addWidget(unhappy_importance_label, 0, 1)
        unhappy_grid.addLayout(self.importance_group, 1, 1)
        unhappy_grid.setVerticalSpacing(5)
        left_layout.addLayout(unhappy_grid)

        # Happy Things
        happy_label = QLabel("2 Things You Were Happy About", self)
        happy_label.setStyleSheet("font: bold 10pt 'Comic Sans MS'; color: #006400;")
        left_layout.addWidget(happy_label)
        self.happy1_entry = QTextEdit(self)
        self.happy1_entry.setMaximumHeight(80)
        self.happy1_entry.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #006666; background-color: rgba(255, 255, 255, 0.8);")
        self.happy2_entry = QTextEdit(self)
        self.happy2_entry.setMaximumHeight(80)
        self.happy2_entry.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #006666; background-color: rgba(255, 255, 255, 0.8);")
        happy_hbox = QHBoxLayout()
        happy_hbox.addWidget(self.happy1_entry)
        happy_hbox.addWidget(self.happy2_entry)
        left_layout.addLayout(happy_hbox)

        # --- Today's Tasks (MoSCoW) Section ---
        tasks_label = QLabel("Today's Tasks (MoSCoW)", self)
        tasks_label.setStyleSheet("font: bold 14pt 'Comic Sans MS'; color: #8B0000;")
        left_layout.addWidget(tasks_label)

        must_label = QLabel("Must Have", self)
        must_label.setStyleSheet("font: bold 10pt 'Comic Sans MS'; color: #006400;")
        self.must_entry = QLineEdit(self)
        self.must_entry.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #006666; background-color: rgba(255, 255, 255, 0.8);")
        must_hbox = QHBoxLayout()
        must_hbox.addWidget(must_label)
        must_hbox.addWidget(self.must_entry)
        left_layout.addLayout(must_hbox)

        should_label = QLabel("Should Have", self)
        should_label.setStyleSheet("font: bold 10pt 'Comic Sans MS'; color: #006400;")
        self.should_entry = QLineEdit(self)
        self.should_entry.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #006666; background-color: rgba(255, 255, 255, 0.8);")
        should_hbox = QHBoxLayout()
        should_hbox.addWidget(should_label)
        should_hbox.addWidget(self.should_entry)
        left_layout.addLayout(should_hbox)

        could_label = QLabel("Could Have", self)
        could_label.setStyleSheet("font: bold 10pt 'Comic Sans MS'; color: #006400;")
        self.could_entry = QLineEdit(self)
        self.could_entry.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #006666; background-color: rgba(255, 255, 255, 0.8);")
        could_hbox = QHBoxLayout()
        could_hbox.addWidget(could_label)
        could_hbox.addWidget(self.could_entry)
        left_layout.addLayout(could_hbox)

        wont_label = QLabel("Won't Have", self)
        wont_label.setStyleSheet("font: bold 10pt 'Comic Sans MS'; color: #006400;")
        self.wont_entry = QLineEdit(self)
        self.wont_entry.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #006666; background-color: rgba(255, 255, 255, 0.8);")
        wont_hbox = QHBoxLayout()
        wont_hbox.addWidget(wont_label)
        wont_hbox.addWidget(self.wont_entry)
        left_layout.addLayout(wont_hbox)

        notes_label = QLabel("Notes from Today", self)
        notes_label.setStyleSheet("font: bold 14pt 'Comic Sans MS'; color: #8B0000;")
        left_layout.addWidget(notes_label)
        self.notes_text = QTextEdit(self)
        self.notes_text.setMaximumHeight(100)
        self.notes_text.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #006666; background-color: rgba(255, 255, 255, 0.8);")
        left_layout.addWidget(self.notes_text)

        # --- Daily Stats Section ---
        stats_label = QLabel("Daily Stats", self)
        stats_label.setStyleSheet("font: bold 14pt 'Comic Sans MS'; color: #8B0000;")
        right_layout.addWidget(stats_label)

        stats_labels_layout = QHBoxLayout()
        nap_hours_label = QLabel("Hours of Nap", self)
        nap_hours_label.setStyleSheet("font: bold 10pt 'Comic Sans MS'; color: #006400;")
        stats_labels_layout.addWidget(nap_hours_label)
        meals_label = QLabel("No. of Meals", self)
        meals_label.setStyleSheet("font: bold 10pt 'Comic Sans MS'; color: #006400;")
        stats_labels_layout.addWidget(meals_label)
        money_label = QLabel("Money Spent ($)", self)
        money_label.setStyleSheet("font: bold 10pt 'Comic Sans MS'; color: #006400;")
        stats_labels_layout.addWidget(money_label)
        right_layout.addLayout(stats_labels_layout)

        stats_entries_layout = QHBoxLayout()
        self.nap_hours_entry = QLineEdit(self)
        self.nap_hours_entry.setMaximumWidth(100)
        self.nap_hours_entry.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #006666; background-color: rgba(255, 255, 255, 0.8);")
        stats_entries_layout.addWidget(self.nap_hours_entry)
        self.meals_entry = QLineEdit(self)
        self.meals_entry.setMaximumWidth(100)
        self.meals_entry.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #006666; background-color: rgba(255, 255, 255, 0.8);")
        stats_entries_layout.addWidget(self.meals_entry)
        self.money_entry = QLineEdit(self)
        self.money_entry.setMaximumWidth(100)
        self.money_entry.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #006666; background-color: rgba(255, 255, 255, 0.8);")
        stats_entries_layout.addWidget(self.money_entry)
        right_layout.addLayout(stats_entries_layout)

        time_wasters_label = QLabel("Time Wasters Today", self)
        time_wasters_label.setStyleSheet("font: bold 10pt 'Comic Sans MS'; color: #006400;")
        right_layout.addWidget(time_wasters_label)
        self.time_wasters_entry = QLineEdit(self)
        self.time_wasters_entry.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #006666; background-color: rgba(255, 255, 255, 0.8);")
        right_layout.addWidget(self.time_wasters_entry)

        # --- Tomorrow's Plan Section ---
        tomorrow_label = QLabel("Tomorrow's Plan", self)
        tomorrow_label.setStyleSheet("font: bold 14pt 'Comic Sans MS'; color: #8B0000;")
        right_layout.addWidget(tomorrow_label)

        tasks_tomorrow_label = QLabel("3 Tasks for Tomorrow", self)
        tasks_tomorrow_label.setStyleSheet("font: bold 10pt 'Comic Sans MS'; color: #006400;")
        right_layout.addWidget(tasks_tomorrow_label)
        self.task1_entry = QLineEdit(self)
        self.task1_entry.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #006666; background-color: rgba(255, 255, 255, 0.8);")
        self.task1_entry.setPlaceholderText("1)")
        right_layout.addWidget(self.task1_entry)
        self.task2_entry = QLineEdit(self)
        self.task2_entry.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #006666; background-color: rgba(255, 255, 255, 0.8);")
        self.task2_entry.setPlaceholderText("2)")
        right_layout.addWidget(self.task2_entry)
        self.task3_entry = QLineEdit(self)
        self.task3_entry.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #006666; background-color: rgba(255, 255, 255, 0.8);")
        self.task3_entry.setPlaceholderText("3)")
        right_layout.addWidget(self.task3_entry)

        mistakes_label = QLabel("Mistakes to Avoid Tomorrow", self)
        mistakes_label.setStyleSheet("font: bold 10pt 'Comic Sans MS'; color: #006400;")
        right_layout.addWidget(mistakes_label)
        self.mistakes_entry = QLineEdit(self)
        self.mistakes_entry.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #006666; background-color: rgba(255, 255, 255, 0.8);")
        right_layout.addWidget(self.mistakes_entry)

        change_label = QLabel("3 Things to Change About Yourself", self)
        change_label.setStyleSheet("font: bold 10pt 'Comic Sans MS'; color: #006400;")
        right_layout.addWidget(change_label)
        self.change1_entry = QLineEdit(self)
        self.change1_entry.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #006666; background-color: rgba(255, 255, 255, 0.8);")
        self.change1_entry.setPlaceholderText("1)")
        right_layout.addWidget(self.change1_entry)
        self.change2_entry = QLineEdit(self)
        self.change2_entry.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #006666; background-color: rgba(255, 255, 255, 0.8);")
        self.change2_entry.setPlaceholderText("2)")
        right_layout.addWidget(self.change2_entry)
        self.change3_entry = QLineEdit(self)
        self.change3_entry.setStyleSheet("font: 10pt 'Comic Sans MS'; color: #006666; background-color: rgba(255, 255, 255, 0.8);")
        self.change3_entry.setPlaceholderText("3)")
        right_layout.addWidget(self.change3_entry)

        # --- Did Today Section ---
        did_today_label = QLabel("Did Today:", self)
        did_today_label.setStyleSheet("font: bold 14pt 'Comic Sans MS'; color: #8B0000;")
        right_layout.addWidget(did_today_label)

        did_today_row1 = QHBoxLayout()
        self.coding_check = QCheckBox("Coding", self)
        self.coding_check.setStyleSheet("font: 12pt 'Comic Sans MS'; color: #800080;")
        did_today_row1.addWidget(self.coding_check)
        self.gate_check = QCheckBox("Gate Classes", self)
        self.gate_check.setStyleSheet("font: 12pt 'Comic Sans MS'; color: #800080;")
        did_today_row1.addWidget(self.gate_check)
        self.speaking_check = QCheckBox("Speaking Skills", self)
        self.speaking_check.setStyleSheet("font: 12pt 'Comic Sans MS'; color: #800080;")
        did_today_row1.addWidget(self.speaking_check)
        right_layout.addLayout(did_today_row1)

        did_today_row2 = QHBoxLayout()
        self.workout_check = QCheckBox("Walk/Workout", self)
        self.workout_check.setStyleSheet("font: 12pt 'Comic Sans MS'; color: #800080;")
        did_today_row2.addWidget(self.workout_check)
        self.meditation_check = QCheckBox("Meditation", self)
        self.meditation_check.setStyleSheet("font: 12pt 'Comic Sans MS'; color: #800080;")
        did_today_row2.addWidget(self.meditation_check)
        right_layout.addLayout(did_today_row2)

        # Add spacing between Did Today and buttons
        right_layout.addSpacing(20)

        # --- Buttons Section ---
        save_button = QPushButton("Save Entry", self)
        save_button.setStyleSheet("background-color: green; color: white; font: 12pt 'Comic Sans MS';")
        save_button.clicked.connect(self.save_data)
        right_layout.addWidget(save_button)

        graph_button = QPushButton("Show Graph", self)
        graph_button.setStyleSheet("background-color: blue; color: white; font: 12pt 'Comic Sans MS';")
        graph_button.clicked.connect(self.plot_data)
        right_layout.addWidget(graph_button)

        # --- Quote of the Day ---
        self.quotes = [f"Quote of the Day {i}: Keep shining!" for i in range(1, 366)]
        day_of_year = datetime.now().timetuple().tm_yday - 1
        quote_label = QLabel(self.quotes[day_of_year], self)
        quote_label.setStyleSheet("font: italic 12pt 'Comic Sans MS'; color: #006666; padding: 5px;")
        quote_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        quote_label.setWordWrap(True)
        quote_label.setFixedWidth(220)
        center_layout.addStretch(2)
        center_layout.addWidget(quote_label)
        center_layout.addStretch(1)

    def load_background_image(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                img_data = BytesIO(response.content)
                image = QImage.fromData(img_data.read())
                pixmap = QPixmap.fromImage(image).scaled(1200, 800)
                background_label = QLabel(self)
                background_label.setPixmap(pixmap)
                background_label.setGeometry(0, 0, 1200, 700)
                background_label.lower()
                print("Background image set.")
            else:
                print(f"Failed to load image. Status code: {response.status_code}")
                self.setStyleSheet("background-color: #F5D6BA;")
        except Exception as e:
            print(f"Error loading image: {e}")
            self.setStyleSheet("background-color: #F5D6BA;")

    def save_data(self):
        if self.radio_important.isChecked():
            unhappy_importance = "important"
        elif self.radio_not_important.isChecked():
            unhappy_importance = "not important"
        else:
            unhappy_importance = "should not care"

        data = {
            'Date': [datetime.now().strftime("%Y-%m-%d")],
            'Task1_Tomorrow': [self.task1_entry.text()],
            'Task2_Tomorrow': [self.task2_entry.text()],
            'Task3_Tomorrow': [self.task3_entry.text()],
            'Happiness_Score': [self.happiness_slider.value()],
            'Productivity_Score': [self.productivity_slider.value()],
            'Must_Have': [self.must_entry.text()],
            'Should_Have': [self.should_entry.text()],
            'Could_Have': [self.could_entry.text()],
            'Wont_Have': [self.wont_entry.text()],
            'Unhappy_Reason': [self.unhappy_reason_entry.toPlainText().strip()],
            'Unhappy_Importance': [unhappy_importance],
            'Happy_Thing1': [self.happy1_entry.toPlainText().strip()],
            'Happy_Thing2': [self.happy2_entry.toPlainText().strip()],
            'Change1': [self.change1_entry.text()],
            'Change2': [self.change2_entry.text()],
            'Change3': [self.change3_entry.text()],
            'Time_Wasters': [self.time_wasters_entry.text()],
            'Mistakes': [self.mistakes_entry.text()],
            'Meals': [self.meals_entry.text()],
            'Money_Spent': [self.money_entry.text()],
            'Nap_Hours': [self.nap_hours_entry.text()],
            'Did_Coding': [self.coding_check.isChecked()],
            'Gate_Classes': [self.gate_check.isChecked()],
            'Speaking_Skills': [self.speaking_check.isChecked()],
            'Workout': [self.workout_check.isChecked()],
            'Meditation': [self.meditation_check.isChecked()],
            'Notes': [self.notes_text.toPlainText().strip()]
        }

        df = pd.DataFrame(data)
        try:
            df.to_csv('diary_data.csv', mode='a', header=not os.path.exists('diary_data.csv'), index=False)
            QMessageBox.information(self, "Success", "Diary entry saved successfully!")
        except PermissionError:
            QMessageBox.critical(self, "Permission Error", 
                                 "Cannot save to 'diary_data.csv'. It may be open elsewhere or you lack permissions.")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"An error occurred while saving: {str(e)}")

    def plot_data(self):
        try:
            df = pd.read_csv('diary_data.csv', on_bad_lines='skip')
            if df.empty:
                QMessageBox.warning(self, "Data Error", "No data available to plot!")
                return

            # Convert Date to datetime for better handling
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values('Date')  # Ensure data is sorted by date
            total_days = len(df['Date'].unique())

            # --- Figure 1: Productivity & Happiness Trends ---
            fig1 = plt.figure(figsize=(6, 4), facecolor='none')
            fig1.patch.set_alpha(0)  # Transparent background
            ax1 = fig1.add_subplot(111)
            ax1.patch.set_alpha(0)  # Transparent axes background
            ax1.plot(df['Date'], df['Happiness_Score'], marker='o', label='Happiness', color='#ff6f61', linewidth=1.5)
            ax1.plot(df['Date'], df['Productivity_Score'], marker='o', label='Productivity', color='#6b5b95', linewidth=1.5)
            ax1.set_title('Happiness & Productivity', fontsize=12, color='#333333')
            ax1.set_xlabel('Date', fontsize=10)
            ax1.set_ylabel('Score (1-5)', fontsize=10)
            ax1.legend(loc='upper left', fontsize=8, frameon=True, facecolor='#ffffff', edgecolor='#2f4f4f')
            ax1.set_xticks(df['Date'])
            ax1.tick_params(axis='x', rotation=45, labelsize=8)
            ax1.set_ylim(0, max(df[['Happiness_Score', 'Productivity_Score']].max()) + 1)
            for spine in ax1.spines.values():
                spine.set_edgecolor('#333333')
                spine.set_linewidth(0.5)
            plt.tight_layout()

            # --- Figure 2: Nap Hours (Scatter Plot) ---
            fig2 = plt.figure(figsize=(6, 3), facecolor='none')
            fig2.patch.set_alpha(0)  # Transparent background
            ax2 = fig2.add_subplot(111)
            ax2.set_facecolor('#ff6f61')  # Red background
            ax2.patch.set_alpha(0.3)  # Set transparency for red background
            ax2.axhspan(5, 8.5, facecolor='#88d8b0', alpha=0.3, label='Healthy Zone (5-8.5h)')  # Green zone with transparency
            ax2.scatter(df['Date'], df['Nap_Hours'].astype(float), color='black', s=50, label='Nap Hours')
            ax2.set_title('Nap Hours', fontsize=12, color='#333333')
            ax2.set_xlabel('Date', fontsize=10)
            ax2.set_ylabel('Hours', fontsize=10)
            ax2.legend(loc='upper left', fontsize=8, frameon=True, facecolor='#ffffff', edgecolor='#2f4f4f')
            ax2.set_xticks(df['Date'])
            ax2.tick_params(axis='x', rotation=45, labelsize=8)
            ax2.set_ylim(0, max(df['Nap_Hours'].astype(float)) + 1)
            for spine in ax2.spines.values():
                spine.set_edgecolor('#333333')
                spine.set_linewidth(1.5)
            plt.tight_layout()

            # --- Figure 3: Pie Charts ---
            fig3 = plt.figure(figsize=(8, 6), facecolor='none')
            fig3.patch.set_alpha(0)  # Transparent background
            activity_cols = ['Did_Coding', 'Gate_Classes', 'Speaking_Skills', 'Workout', 'Meditation']

            # Row 1: 2 Pie Charts
            ax3 = fig3.add_axes([0.05, 0.7, 0.3, 0.25], aspect='equal')
            ax3.patch.set_alpha(0)  # Transparent axes background
            done = df[activity_cols[0]].sum()
            not_done = total_days - done
            ax3.pie([done, not_done], labels=['Done', 'Not Done'], colors=['#88d8b0', '#ffcc5c'], 
                    autopct='%1.1f%%', startangle=90, textprops={'fontsize': 8})
            ax3.set_title(f'{activity_cols[0].replace("Did_", "")}', fontsize=10, color='#333333', y=1.1)

            ax4 = fig3.add_axes([0.45, 0.7, 0.3, 0.25], aspect='equal')
            ax4.patch.set_alpha(0)  # Transparent axes background
            done = df[activity_cols[1]].sum()
            not_done = total_days - done
            ax4.pie([done, not_done], labels=['Done', 'Not Done'], colors=['#88d8b0', '#ffcc5c'], 
                    autopct='%1.1f%%', startangle=90, textprops={'fontsize': 8})
            ax4.set_title(f'{activity_cols[1].replace("Did_", "")}', fontsize=10, color='#333333', y=1.1)

            # Row 2: 2 Pie Charts
            ax5 = fig3.add_axes([0.05, 0.35, 0.3, 0.25], aspect='equal')
            ax5.patch.set_alpha(0)  # Transparent axes background
            done = df[activity_cols[2]].sum()
            not_done = total_days - done
            ax5.pie([done, not_done], labels=['Done', 'Not Done'], colors=['#88d8b0', '#ffcc5c'], 
                    autopct='%1.1f%%', startangle=90, textprops={'fontsize': 8})
            ax5.set_title(f'{activity_cols[2].replace("Did_", "")}', fontsize=10, color='#333333', y=1.1)

            ax6 = fig3.add_axes([0.45, 0.35, 0.3, 0.25], aspect='equal')
            ax6.patch.set_alpha(0)  # Transparent axes background
            done = df[activity_cols[3]].sum()
            not_done = total_days - done
            ax6.pie([done, not_done], labels=['Done', 'Not Done'], colors=['#88d8b0', '#ffcc5c'], 
                    autopct='%1.1f%%', startangle=90, textprops={'fontsize': 8})
            ax6.set_title(f'{activity_cols[3].replace("Did_", "")}', fontsize=10, color='#333333', y=1.1)

            # Row 3: 1 Pie Chart
            ax7 = fig3.add_axes([0.25, 0.05, 0.3, 0.25], aspect='equal')
            ax7.patch.set_alpha(0)  # Transparent axes background
            done = df[activity_cols[4]].sum()
            not_done = total_days - done
            ax7.pie([done, not_done], labels=['Done', 'Not Done'], colors=['#88d8b0', '#ffcc5c'], 
                    autopct='%1.1f%%', startangle=90, textprops={'fontsize': 8})
            ax7.set_title(f'{activity_cols[4].replace("Did_", "")}', fontsize=10, color='#333333', y=1.1)

            plt.tight_layout()

            # Show all figures
            plt.show()

        except FileNotFoundError:
            QMessageBox.warning(self, "File Error", "No data found. Start writing your diary first!")
        except Exception as e:
            QMessageBox.critical(self, "Plot Error", f"An error occurred while plotting: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiaryWindow()
    window.show()
    sys.exit(app.exec())