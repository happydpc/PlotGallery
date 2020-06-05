from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QCheckBox, QCommandLinkButton, QVBoxLayout
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.Qt3DCore import QEntity
from PyQt5.Qt3DExtras import Qt3DWindow, QFirstPersonCameraController
from PyQt5.Qt3DExtras import QTorusMesh, QPhongMaterial, QConeMesh, QCylinderMesh, QCuboidMesh, QPlaneMesh, QSphereMesh, Qt3DWindow, QFirstPersonCameraController
# ModuleNotFoundError: No module named 'PyQt5.Qt3DExtras'
# Failed to make context current: OpenGL resources will not be destroyed
import sys


class contained3dWindow(QWidget):
    def __init__(self):
        super().__init__()
        lay = QVBoxLayout(self)
        self.view = Qt3DWindow()
        container = QWidget.createWindowContainer(self.view)
        lay.addWidget(container)
        self.rootEntity = QEntity()
        cameraEntity = self.view.camera()
        camController = QFirstPersonCameraController(self.rootEntity)
        camController.setCamera(cameraEntity)
        self.view.setRootEntity(self.rootEntity)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Generated by pyuic
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1416, 1041)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(
            QtCore.QRect(250, 160, 1051, 721))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1416, 38))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Source of the problem. Error occurs when the contained3dWindow instance is created
        c_window = contained3dWindow()
        self.verticalLayout.addWidget(c_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())
