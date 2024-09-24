import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QMessageBox, QLabel, QSystemTrayIcon, QMenu
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QIcon, QImage, QAction
from PySide6.QtCore import Qt, QRect, QSize, QTimer
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtCore import QUrl
import pyautogui
from PIL import Image

class ScreenshotTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.screenshot = None
        self.start_point = None
        self.end_point = None
        self.initSounds()
        self.initSystemTray()

    def initUI(self):
        self.setWindowTitle('Awesome Screenshot Tool')
        self.setGeometry(100, 100, 400, 300)
        self.setWindowIcon(self.loadIcon('Icons/screenshot_icon.png'))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        button_layout = QVBoxLayout()

        self.capture_btn = QPushButton('Capture Screenshot', self)
        self.capture_btn.setIcon(self.loadIcon('Icons/camera_icon.png'))
        self.capture_btn.clicked.connect(self.prepare_screenshot)
        button_layout.addWidget(self.capture_btn)

        self.save_btn = QPushButton('Save Screenshot', self)
        self.save_btn.setIcon(self.loadIcon('Icons/save_icon.png'))
        self.save_btn.clicked.connect(self.save_screenshot)
        self.save_btn.setEnabled(False)
        button_layout.addWidget(self.save_btn)

        main_layout.addLayout(button_layout)

        self.preview_label = QLabel(self)
        self.preview_label.setFixedSize(200, 200)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setText("Captured image preview")
        self.preview_label.setStyleSheet("border: 2px dashed gray;")
        main_layout.addWidget(self.preview_label)

        central_widget.setLayout(main_layout)

    def loadIcon(self, path):
        if os.path.exists(path):
            return QIcon(path)
        else:
            print(f"Warning: Icon not found: {path}")
            return QIcon()

    def initSounds(self):
        self.capture_sound = self.loadSound("Audio/camera_shutter.wav")
        self.success_sound = self.loadSound("Audio/success_chime.wav")
        self.fail_sound = self.loadSound("Audio/fail_buzz.wav")

    def loadSound(self, path):
        sound = QSoundEffect()
        if os.path.exists(path):
            sound.setSource(QUrl.fromLocalFile(path))
            if sound.status() == QSoundEffect.Error:
                print(f"Error: Unable to load sound file: {path}")
                return None
            return sound
        else:
            print(f"Warning: Sound file not found: {path}")
            return None

    def playSound(self, sound):
        if sound and sound.status() == QSoundEffect.Ready:
            sound.play()

    def initSystemTray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.windowIcon())
        
        # Create the tray menu
        tray_menu = QMenu()
        
        capture_action = QAction("Capture", self)
        capture_action.triggered.connect(self.prepare_screenshot)
        tray_menu.addAction(capture_action)
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        tray_menu.addAction(about_action)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_application)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
        self.tray_icon.show()

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.prepare_screenshot()

    def show_about(self):
        about_html = """
        <html>
        <body>
            <h2>Shane's ScreenCapper Tool</h2>
            <p>Version 1.0</p>
            <p>A simple and powerful screenshot capture tool.</p>
            <p>by Ryon Shane Hall</p>
            <p><a href="https://github.com/endorpheus">https://github.com/endorpheus</a></p>
        </body>
        </html>
        """
        QMessageBox.about(self, "About ScreenCapper", about_html)

    def quit_application(self):
        QApplication.quit()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def prepare_screenshot(self):
        self.hide()
        QTimer.singleShot(500, self.capture_screenshot)  # Wait 500ms before capturing

    def capture_screenshot(self):
        self.screenshot = pyautogui.screenshot()
        self.playSound(self.capture_sound)
        self.show_fullscreen_window()

    def show_fullscreen_window(self):
        self.fullscreen_window = FullscreenWindow(self.screenshot, self)
        self.fullscreen_window.showFullScreen()

    def update_preview(self):
        if self.screenshot and self.start_point and self.end_point:
            x1, y1 = min(self.start_point.x(), self.end_point.x()), min(self.start_point.y(), self.end_point.y())
            x2, y2 = max(self.start_point.x(), self.end_point.x()), max(self.start_point.y(), self.end_point.y())
            cropped_image = self.screenshot.crop((x1, y1, x2, y2))
            
            # Convert PIL Image to RGB mode
            rgb_image = cropped_image.convert('RGB')
            
            # Convert PIL Image to QImage
            qimage = QImage(rgb_image.tobytes(), rgb_image.width, rgb_image.height, QImage.Format_RGB888)
            
            pixmap = QPixmap.fromImage(qimage)
            
            # Scale the pixmap to fit in the preview label while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(QSize(200, 200), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Create a new pixmap with a white background
            background = QPixmap(200, 200)
            background.fill(Qt.white)
            
            # Create a painter to draw the scaled pixmap onto the background
            painter = QPainter(background)
            painter.drawPixmap((200 - scaled_pixmap.width()) // 2, (200 - scaled_pixmap.height()) // 2, scaled_pixmap)
            painter.end()
            
            self.preview_label.setPixmap(background)
            self.preview_label.setStyleSheet("border: 2px solid green;")

    def save_screenshot(self):
        if self.screenshot and self.start_point and self.end_point:
            file_dialog = QFileDialog(self)
            file_dialog.setWindowTitle("Save Screenshot")
            file_dialog.setAcceptMode(QFileDialog.AcceptSave)
            file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")
            file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
            file_dialog.setViewMode(QFileDialog.List)
            file_dialog.setFileMode(QFileDialog.AnyFile)
            
            if file_dialog.exec() == QFileDialog.Accepted:
                file_path = file_dialog.selectedFiles()[0]
                if file_path:
                    x1, y1 = min(self.start_point.x(), self.end_point.x()), min(self.start_point.y(), self.end_point.y())
                    x2, y2 = max(self.start_point.x(), self.end_point.x()), max(self.start_point.y(), self.end_point.y())
                    cropped_image = self.screenshot.crop((x1, y1, x2, y2))
                    cropped_image.save(file_path)
                    self.playSound(self.success_sound)
                    QMessageBox.information(self, "Success", "Screenshot saved successfully!")
                else:
                    self.playSound(self.fail_sound)
                    QMessageBox.warning(self, "Warning", "Save operation cancelled.")
            else:
                self.playSound(self.fail_sound)
                QMessageBox.warning(self, "Warning", "Save operation cancelled.")
        else:
            self.playSound(self.fail_sound)
            QMessageBox.warning(self, "Warning", "No area selected for saving.")

class FullscreenWindow(QWidget):
    def __init__(self, screenshot, parent):
        super().__init__()
        self.parent = parent
        self.screenshot = screenshot
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.showFullScreen()
        self.setMouseTracking(True)
        self.start_point = None
        self.end_point = None
        self.drawing = False

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap.fromImage(self.screenshot.toqimage())
        painter.drawPixmap(self.rect(), pixmap)

        if self.drawing and self.start_point and self.end_point:
            painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.SolidLine))
            painter.drawRect(QRect(self.start_point, self.end_point))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = event.position().toPoint()
            self.drawing = True

    def mouseMoveEvent(self, event):
        if self.drawing:
            self.end_point = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end_point = event.position().toPoint()
            self.drawing = False
            self.parent.start_point = self.start_point
            self.parent.end_point = self.end_point
            self.parent.save_btn.setEnabled(True)
            self.parent.update_preview()
            self.close()
            self.parent.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tool = ScreenshotTool()
    tool.show()
    sys.exit(app.exec())