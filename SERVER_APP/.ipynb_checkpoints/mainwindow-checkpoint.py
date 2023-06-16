# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
                               QLabel, QMainWindow, QPlainTextEdit, QPushButton,
                               QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(932, 901)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_4 = QFrame(self.centralwidget)
        self.frame_4.setObjectName(u"frame_4")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setFrameShape(QFrame.Box)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.frame_4)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.port_combobox = QComboBox(self.frame_3)
        self.port_combobox.setObjectName(u"port_combobox")
        self.port_combobox.setMinimumSize(QSize(90, 0))

        self.horizontalLayout_2.addWidget(self.port_combobox)

        self.button1 = QPushButton(self.frame_3)
        self.button1.setObjectName(u"button1")

        self.horizontalLayout_2.addWidget(self.button1)

        self.horizontalLayout_3.addWidget(self.frame_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.frame_2 = QFrame(self.frame_4)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.mode = QLabel(self.frame_2)
        self.mode.setObjectName(u"mode")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.mode.sizePolicy().hasHeightForWidth())
        self.mode.setSizePolicy(sizePolicy1)
        self.mode.setMaximumSize(QSize(16777215, 25))
        self.mode.setStyleSheet(u"background-color: rgb(255, 255, 127);")
        self.mode.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.mode)

        self.battery = QLabel(self.frame_2)
        self.battery.setObjectName(u"battery")
        sizePolicy1.setHeightForWidth(self.battery.sizePolicy().hasHeightForWidth())
        self.battery.setSizePolicy(sizePolicy1)
        self.battery.setMaximumSize(QSize(16777215, 25))
        self.battery.setStyleSheet(u"background-color: rgb(255, 255, 127);")
        self.battery.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.battery)

        self.send_queue_size = QLabel(self.frame_2)
        self.send_queue_size.setObjectName(u"send_queue_size")
        sizePolicy1.setHeightForWidth(self.send_queue_size.sizePolicy().hasHeightForWidth())
        self.send_queue_size.setSizePolicy(sizePolicy1)
        self.send_queue_size.setMaximumSize(QSize(16777215, 25))
        self.send_queue_size.setStyleSheet(u"background-color: rgb(255, 255, 127);")
        self.send_queue_size.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.send_queue_size)

        self.horizontalSpacer_2 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.ch1_status = QLabel(self.frame_2)
        self.ch1_status.setObjectName(u"ch1_status")
        sizePolicy1.setHeightForWidth(self.ch1_status.sizePolicy().hasHeightForWidth())
        self.ch1_status.setSizePolicy(sizePolicy1)
        self.ch1_status.setMaximumSize(QSize(16777215, 25))
        self.ch1_status.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.ch1_status.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.ch1_status)

        self.ch2_status = QLabel(self.frame_2)
        self.ch2_status.setObjectName(u"ch2_status")
        sizePolicy1.setHeightForWidth(self.ch2_status.sizePolicy().hasHeightForWidth())
        self.ch2_status.setSizePolicy(sizePolicy1)
        self.ch2_status.setMaximumSize(QSize(16777215, 25))
        self.ch2_status.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.ch2_status.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.ch2_status)

        self.ref_status = QLabel(self.frame_2)
        self.ref_status.setObjectName(u"ref_status")
        self.ref_status.setMaximumSize(QSize(16777215, 25))
        self.ref_status.setStyleSheet(u"background-color: rgb(255, 0, 0);")
        self.ref_status.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.ref_status)

        self.horizontalLayout_3.addWidget(self.frame_2)

        self.verticalLayout.addWidget(self.frame_4)

        self.graph_1_frame = QFrame(self.centralwidget)
        self.graph_1_frame.setObjectName(u"graph_1_frame")
        self.graph_1_frame.setFrameShape(QFrame.Box)
        self.graph_1_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.graph_1_frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.graph_1_layout = QVBoxLayout()
        self.graph_1_layout.setObjectName(u"graph_1_layout")

        self.verticalLayout_3.addLayout(self.graph_1_layout)

        self.verticalLayout.addWidget(self.graph_1_frame)

        self.graph_2_frame = QFrame(self.centralwidget)
        self.graph_2_frame.setObjectName(u"graph_2_frame")
        self.graph_2_frame.setFrameShape(QFrame.Box)
        self.graph_2_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.graph_2_frame)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.graph_2_layout = QVBoxLayout()
        self.graph_2_layout.setObjectName(u"graph_2_layout")

        self.verticalLayout_6.addLayout(self.graph_2_layout)

        self.verticalLayout.addWidget(self.graph_2_frame)

        self.graph_ppg_frame = QFrame(self.centralwidget)
        self.graph_ppg_frame.setObjectName(u"graph_ppg_frame")
        self.graph_ppg_frame.setFrameShape(QFrame.Box)
        self.graph_ppg_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.graph_ppg_frame)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.graph_ppg_layout = QVBoxLayout()
        self.graph_ppg_layout.setObjectName(u"graph_ppg_layout")

        self.verticalLayout_7.addLayout(self.graph_ppg_layout)

        self.verticalLayout.addWidget(self.graph_ppg_frame)

        self.graph_spectrum_frame = QFrame(self.centralwidget)
        self.graph_spectrum_frame.setObjectName(u"graph_spectrum_frame")
        self.graph_spectrum_frame.setFrameShape(QFrame.Box)
        self.graph_spectrum_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.graph_spectrum_frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.graph_spectrum_layout = QVBoxLayout()
        self.graph_spectrum_layout.setObjectName(u"graph_spectrum_layout")

        self.verticalLayout_4.addLayout(self.graph_spectrum_layout)

        self.verticalLayout.addWidget(self.graph_spectrum_frame)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.info = QPlainTextEdit(self.frame)
        self.info.setObjectName(u"info")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.info.sizePolicy().hasHeightForWidth())
        self.info.setSizePolicy(sizePolicy2)
        self.info.setMaximumSize(QSize(16777215, 120))

        self.verticalLayout_2.addWidget(self.info)

        self.verticalLayout.addWidget(self.frame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"nnfx2 \ub1cc\ud30c\uce21\uc815", None))
        self.button1.setText(QCoreApplication.translate("MainWindow", u"\uae30\uae30\uc5f0\uacb0", None))
        self.mode.setText(QCoreApplication.translate("MainWindow", u"\uc5f0\uacb0\ub300\uae30", None))
        self.battery.setText(QCoreApplication.translate("MainWindow", u"??%", None))
        self.send_queue_size.setText(QCoreApplication.translate("MainWindow", u"Queue:0", None))
        self.ch1_status.setText(QCoreApplication.translate("MainWindow", u"CH1 \ubd80\ucc29\uc0c1\ud0dc", None))
        self.ch2_status.setText(QCoreApplication.translate("MainWindow", u"CH2 \ubd80\ucc29\uc0c1\ud0dc", None))
        self.ref_status.setText(
            QCoreApplication.translate("MainWindow", u"\uadd3\ubcfc \ubd80\ucc29\uc0c1\ud0dc", None))
        self.info.setPlainText("")
    # retranslateUi
