import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap, QFont, QColor, QPalette
from PyQt5.QtCore import Qt

class DALL_E_Client(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IC Auto Image Generator")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #060420; color: #FFFFFF;")

        # Set up a dark and modern theme
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(6, 4, 32))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

        # Create and style widgets
        font = QFont("Arial", 18, QFont.Bold)

        self.input_text = QLineEdit(self)
        self.input_text.setPlaceholderText("Insert Content here")
        self.input_text.setFont(font)
        self.input_text.setStyleSheet(
            "background-color: #0C3257; color: #FFFFFF; border: 2px solid #0C3257; border-radius: 10px;"
            "padding: 10px;"
        )

        buttons_stylesheet = (
            "QPushButton {"
            "   background-color: #1F5EA8; color: #FFFFFF; border: none; border-radius: 10px; padding: 10px;"
            "   min-width: 100px;"
            "}"
            "QPushButton:hover {"
            "   border: 2px solid #FFFFFF;"
            "}"
        )

        self.send_button = QPushButton("Send", self)
        self.send_button.setFont(font)
        self.send_button.setCursor(Qt.PointingHandCursor)  # Show a pointing hand cursor on hover
        self.send_button.setFocusPolicy(Qt.NoFocus)  # Remove the dotted border on click
        self.send_button.setStyleSheet(buttons_stylesheet)
        self.send_button.clicked.connect(self.send_request)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.save_button = QPushButton("Save Image", self)
        self.save_button.setFont(font)
        self.save_button.setCursor(Qt.PointingHandCursor)  # Show a pointing hand cursor on hover
        self.save_button.setFocusPolicy(Qt.NoFocus)  # Remove the dotted border on click
        self.save_button.setStyleSheet(buttons_stylesheet)
        self.save_button.clicked.connect(self.save_image)

        # Set up layouts
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_text)
        input_layout.addWidget(self.send_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.image_label, 3)  # The image label takes up 3/4 of the space
        main_layout.addWidget(self.save_button)

        self.setLayout(main_layout)

    def send_request(self):
        # Ensure text description is not empty before sending the request
        text_description = self.input_text.text().strip()
        if not text_description:
            return

        api_key = os.environ.get("DALL_E_API_KEY")  # Replace "DALL_E_API_KEY" with your actual environment variable name
        if not api_key:
            print("Error: DALL_E_API_KEY environment variable not set.")
            return

        # Send text description to DALL-E and receive the image URL
        headers = {"Authorization": f"Bearer {api_key}"}
        data = {"text": text_description}
        response = requests.get("https://api.openai.com/v1/davinci/images", params=data, headers=headers)

        if response.ok:
            image_data = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            self.image_label.setPixmap(pixmap)
        else:
            print("Error:", response.status_code, response.text)

    def save_image(self):
        # Save the displayed image to a file
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.jpeg);;All Files (*)",
                                                   options=options)
        if file_name:
            pixmap = self.image_label.pixmap()
            pixmap.save(file_name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DALL_E_Client()
    window.show()
    sys.exit(app.exec_())