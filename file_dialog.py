# coding=utf-8
import sys
from PyQt4 import QtGui, QtCore

reload(sys)
sys.setdefaultencoding('utf-8')


class file_dialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.resize(400, 120)

        # 表格布局，用来布局QLabel和QLineEdit及QSpinBox
        grid = QtGui.QGridLayout()

        layout = QtGui.QHBoxLayout()
        label = QtGui.QLabel(u'源文件夹', parent=self)
        layout.addWidget(label)
        self.leName = QtGui.QLineEdit(parent=self)
        layout.addWidget(self.leName)
        btn1 = QtGui.QPushButton(u'选择', parent=self)
        btn1.clicked.connect(self.select_source_dir)
        layout.addWidget(btn1)
        grid.addLayout(layout, 0, 1, 1, 1)

        layout1 = QtGui.QHBoxLayout()
        label1 = QtGui.QLabel(u'目标文件夹', parent=self)
        layout1.addWidget(label1)
        self.leName1 = QtGui.QLineEdit(parent=self)
        layout1.addWidget(self.leName1)
        btn2 = QtGui.QPushButton(u'选择', parent=self)
        btn2.clicked.connect(self.select_dest_dir)
        layout1.addWidget(btn2)
        grid.addLayout(layout1, 1, 1, 1, 1)

        # 创建ButtonBox，用户确定和取消
        button_box = QtGui.QDialogButtonBox(parent=self)
        button_box.setOrientation(QtCore.Qt.Horizontal)  # 设置为水平方向
        button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)  # 确定和取消两个按钮
        # 连接信号和槽
        button_box.accepted.connect(self.accept)  # 确定
        button_box.rejected.connect(self.reject)  # 取消

        # 垂直布局，布局表格及按钮
        layout3 = QtGui.QVBoxLayout()

        # 加入前面创建的表格布局
        layout3.addLayout(grid)

        # 放一个间隔对象美化布局
        spacerItem = QtGui.QSpacerItem(20, 48, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        layout3.addItem(spacerItem)

        # ButtonBox
        layout3.addWidget(button_box)

        self.setLayout(layout3)

    def source_dir(self):
        return self.leName.text()

    def dest_dir(self):
        return self.leName1.text()

    def select_source_dir(self):
        self.leName.setText(QtGui.QFileDialog.getExistingDirectory())

    def select_dest_dir(self):
        self.leName1.setText(QtGui.QFileDialog.getExistingDirectory())


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWindow = file_dialog()
    mainWindow.show()
    sys.exit(app.exec_())