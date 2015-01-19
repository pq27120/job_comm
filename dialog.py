# coding=utf-8
import sys
from PyQt4 import QtGui, QtCore

class Dialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.resize(120, 120)

        # 表格布局，用来布局QLabel和QLineEdit及QSpinBox
        grid = QtGui.QGridLayout()

        grid.addWidget(QtGui.QLabel('表名', parent=self), 0, 0, 1, 1)

        self.leName = QtGui.QLineEdit(parent=self)
        grid.addWidget(self.leName, 0, 1, 1, 1)

        grid.addWidget(QtGui.QLabel('sql类型', parent=self), 1, 0, 1, 1)

        self.my_combo = QtGui.QComboBox(parent=self)
        self.my_combo.addItem('select')
        self.my_combo.addItem('insert')
        self.my_combo.addItem('update')
        grid.addWidget(self.my_combo, 1, 1, 1, 1)

        # 创建ButtonBox，用户确定和取消
        button_box = QtGui.QDialogButtonBox(parent=self)
        button_box.setOrientation(QtCore.Qt.Horizontal)  # 设置为水平方向
        button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)  # 确定和取消两个按钮
        # 连接信号和槽
        button_box.accepted.connect(self.accept)  # 确定
        button_box.rejected.connect(self.reject)  # 取消

        # 垂直布局，布局表格及按钮
        layout = QtGui.QVBoxLayout()

        # 加入前面创建的表格布局
        layout.addLayout(grid)

        # 放一个间隔对象美化布局
        spacerItem = QtGui.QSpacerItem(20, 48, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        layout.addItem(spacerItem)

        # ButtonBox
        layout.addWidget(button_box)

        self.setLayout(layout)

    def name(self):
        return self.leName.text()

    def sql_type(self):
        return self.my_combo.currentText()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWindow = Dialog()
    mainWindow.show()
    sys.exit(app.exec_())