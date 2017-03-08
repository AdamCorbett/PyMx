import sys
from PySide.QtCore import *
from PySide.QtGui import *
import Mobotix


class MySignal(QObject):
    sig = Signal(str)


class MobotixLoader(QThread):
    def __init__(self, mobotix_cam):
        QThread.__init__(self)
        self.cam = mobotix_cam
        self.signal = MySignal()

    def run(self):
        self.cam.update()
        self.signal.sig.emit('OK')


class Example(QMainWindow):

    def __init__(self, mobotix_cam, mobotix_config):
        super(Example, self).__init__()

        self.timer = None  # type: QTimer
        self.imageLabel = None
        self.scrollArea = None
        self.mobotix_cam = mobotix_cam
        self.config = mobotix_config
        self.mobotix_loader = MobotixLoader(self.mobotix_cam)
        self.mobotix_loader.signal.sig.connect(self.load)

        self.setup_ui()

    def setup_ui(self):

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored,
                                      QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.setCentralWidget(self.scrollArea)

        self.setWindowTitle("Image Viewer")
        self.resize(500, 400)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        # noinspection PyCallByClass
        reply = QMessageBox.question(self, "Message",
                                     "Are you sure you want to quit?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def load(self):
        image = QImage()
        image.loadFromData(self.mobotix_cam.image_data)
        image = image.scaled(self.size(), Qt.IgnoreAspectRatio)

        painter = QPainter()
        painter.begin(image)
        painter.drawEllipse(100, 100, 100, 50)
        painter.drawRect(self.config.sections['events'].items['AS'].activity_area[1:])
        painter.end()

        self.imageLabel.setPixmap(QPixmap.fromImage(image))
        self.imageLabel.adjustSize()

    def run(self, interval=5000):
        self.timer = QTimer()
        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.mobotix_loader.start)
        self.timer.start(interval)


def main():
    app = QApplication(sys.argv)
    cam = Mobotix.MobotixCam()
    cfg = Mobotix.MobotixConfig(cam.get_config().decode('utf-8'))
    ex = Example(cam, cfg)
    ex.run()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
