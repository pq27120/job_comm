# coding=utf-8
import ConfigParser
import os
import sys
from PyQt4 import QtGui, QtCore

reload(sys)
sys.setdefaultencoding('utf-8')


class jdbc_edit_dialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)

        self.resize(300, 200)

        self.init_jdbc_conf()

        grid = QtGui.QGridLayout()

        layout = QtGui.QHBoxLayout()
        label = QtGui.QLabel(u'服务器IP', parent=self)
        layout.addWidget(label)
        self.server_ip_edit = QtGui.QLineEdit(self.server, parent=self)
        layout.addWidget(self.server_ip_edit)
        grid.addLayout(layout, 0, 1, 1, 1)

        layout1 = QtGui.QHBoxLayout()
        label1 = QtGui.QLabel(u'用户名', parent=self)
        layout1.addWidget(label1)
        self.user_name_edit = QtGui.QLineEdit(self.user_name, parent=self)
        layout1.addWidget(self.user_name_edit)
        grid.addLayout(layout1, 1, 1, 1, 1)

        layout2 = QtGui.QHBoxLayout()
        label2 = QtGui.QLabel(u'密码', parent=self)
        layout2.addWidget(label2)
        self.password_edit = QtGui.QLineEdit(self.password, parent=self)
        layout2.addWidget(self.password_edit)
        grid.addLayout(layout2, 2, 1, 1, 1)

        layout3 = QtGui.QHBoxLayout()
        label3 = QtGui.QLabel(u'端口', parent=self)
        layout3.addWidget(label3)
        self.port_edit = QtGui.QLineEdit(self.port, parent=self)
        layout3.addWidget(self.port_edit)
        grid.addLayout(layout3, 3, 1, 1, 1)

        layout4 = QtGui.QHBoxLayout()
        label4 = QtGui.QLabel(u'SID', parent=self)
        layout4.addWidget(label4)
        self.sid_edit = QtGui.QLineEdit(self.sid, parent=self)
        layout4.addWidget(self.sid_edit)
        grid.addLayout(layout4, 4, 1, 1, 1)

        # 创建ButtonBox，用户确定和取消
        button_box = QtGui.QDialogButtonBox(parent=self)
        button_box.setOrientation(QtCore.Qt.Horizontal)  # 设置为水平方向
        button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)  # 确定和取消两个按钮
        # 连接信号和槽
        button_box.accepted.connect(self.accept)  # 确定
        button_box.rejected.connect(self.reject)  # 取消

        # 垂直布局，布局表格及按钮
        layout5 = QtGui.QVBoxLayout()

        # 加入前面创建的表格布局
        layout5.addLayout(grid)

        # 放一个间隔对象美化布局
        spacerItem = QtGui.QSpacerItem(20, 48, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        layout5.addItem(spacerItem)

        # ButtonBox
        layout5.addWidget(button_box)

        self.setLayout(layout5)

    def save(self):
        conf = ConfigParser.ConfigParser()
        conf.read(os.path.join(os.getcwd()) + '/config/jdbc.cfg')
        conf.set("gz_oracle", "username", self.user_name_edit.text())
        conf.set("gz_oracle", "password", self.password_edit.text())
        conf.set("gz_oracle", "server", self.server_ip_edit.text())
        conf.set("gz_oracle", "port", self.port_edit.text())
        conf.set("gz_oracle", "sid", self.sid_edit.text())
        conf.write(open(os.path.join(os.getcwd()) + '/config/jdbc.cfg', "w"))

    def init_jdbc_conf(self):
        conf = ConfigParser.ConfigParser()
        # print  os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))
        conf.read(os.path.join(os.getcwd()) + '/config/jdbc.cfg')
        self.user_name = conf.get('gz_oracle', 'username')
        self.password = conf.get('gz_oracle', 'password')
        self.server = conf.get('gz_oracle', 'server')
        self.port = conf.get('gz_oracle', 'port')
        self.sid = conf.get('gz_oracle', 'sid')


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainWindow = jdbc_edit_dialog()
    mainWindow.show()
    sys.exit(app.exec_())