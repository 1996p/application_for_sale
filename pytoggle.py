from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class PyToggle(QCheckBox):
    def __init__(self, *args, **kwargs):
        QCheckBox.__init__(self, *args, **kwargs)
        self.setCursor(Qt.PointingHandCursor)
        self._bg_color = "#b0b0b0"
        self._circle_color = "#d0d0d0"
        self._active_color = "#00bcff"

        self._circle_position = 3
        self.animation = QPropertyAnimation(self, b"circle_position")
        self.animation.setEasingCurve(QEasingCurve.OutBounce)
        self.animation.setDuration(500)

        self.stateChanged.connect(self.debstar_transitionug)

    def paintEvent(self, e):
        # SETTINGS SIZE

        self.resize(50, 21)
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)

        rect = QRect(0, 0, self.width(), self.height())
        if not self.isChecked():
            p.setBrush(QColor(self._bg_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height())

            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 3, 15, 15)
        else:
            p.setBrush(QColor(self._active_color))
            p.drawRoundedRect(0, 0, rect.width(), self.height(), self.height() / 2, self.height())

            p.setBrush(QColor(self._circle_color))
            p.drawEllipse(self._circle_position, 3, 15, 15)

    @pyqtProperty(float)
    def circle_position(self):
        return self._circle_position

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    def debstar_transitionug(self, value):
        self.animation.stop()
        if value:
            self.animation.setEndValue(self.width() - 19)
        else:
            self.animation.setEndValue(3)
        self.animation.start()

    def hitButton(self, pos=QPoint):
        return self.contentsRect().contains(pos)
