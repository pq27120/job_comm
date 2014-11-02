# coding=utf-8
from Dialog import Dialog
import os

import sys
import shutil
from PyQt4.uic.properties import QtCore
from dialog.jdbc_edit_dialog import jdbc_edit_dialog
from file_dialog import file_dialog

reload(sys)
sys.setdefaultencoding('utf-8')
import socket, cx_Oracle
from PyQt4 import QtGui
import ConfigParser
import decimal


class Frame(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        layout = QtGui.QVBoxLayout()
        toolBar = QtGui.QToolBar()
        simpleButton = QtGui.QToolButton()
        simpleButton.setText(u'贵州')
        simpleButton.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        simpleButton.setMenu(self.pop_file_menu())
        toolBar.addWidget(simpleButton)
        layout.addWidget(toolBar)

        self.menu_bar = QtGui.QMenuBar()
        menu = QtGui.QMenu()
        menu.setTitle(u'贵州')
        action = QtGui.QAction(self)
        action.setText(u'IP限制')
        menu.addAction(action)
        self.menu_bar.addMenu(menu)

        # 创建table和model
        self.table = QtGui.QTableView(parent=self)
        self.model = QtGui.QStandardItemModel(parent=self)
        self.model.setHorizontalHeaderLabels([u'返回值'])
        self.table.setModel(self.model)

        # 创建一个垂直布局，用于防止表格和按钮
        layout.addWidget(self.table)
        self.setLayout(layout)

    def pop_file_menu(self):
        aMenu = QtGui.QMenu(self)
        aMenu.addAction(QtGui.QAction(u'ip添加', self, triggered=self.button_one_clicked))
        aMenu.addAction(QtGui.QAction(u'sql生成', self, triggered=self.show_dialog))
        aMenu.addAction(QtGui.QAction(u'增量包', self, triggered=self.create_war))
        aMenu.addAction(QtGui.QAction(u'jdbc修改', self, triggered=self.jdbc_edit))
        return aMenu

    def show_dialog(self):
        dialog = Dialog(parent=self)
        if dialog.exec_():
            # print dialog.name() + ' ' + dialog.sql_type()
            return_sql = self.create_sql(dialog.name(), dialog.sql_type())
            if self.model.rowCount() > 0:
                self.model.removeRow(self.model.rowCount() - 1)
            self.model.appendRow((
                QtGui.QStandardItem(return_sql)
            ))
            self.table.resizeColumnsToContents()  # 将列调整到跟内容大小相匹配
        dialog.destroy()

    def create_sql(self, input_name, sql_type):
        # print input_name
        conf = ConfigParser.ConfigParser()
        conf.read(os.getcwd() + '/config/jdbc.cfg')
        conn = cx_Oracle.connect(conf.get('gz_oracle', 'username'),
                                 conf.get('gz_oracle', 'password'),
                                 conf.get('gz_oracle', 'server') + ':'
                                 + conf.get('gz_oracle', 'port') + '/'
                                 + conf.get('gz_oracle', 'sid'))
        cursor = conn.cursor()
        cursor.prepare('''select column_name from user_tab_columns where Table_Name = upper(:input_name)''')
        cursor.execute(None, {'input_name': str(input_name)})
        dic = {'select': self.create_select(input_name, cursor),
               'insert': self.create_insert(input_name, cursor),
               'update': self.create_update(input_name, cursor)}
        return dic[str(sql_type)]

    def jdbc_edit(self):
        dialog = jdbc_edit_dialog(parent=self)
        if dialog.exec_():
            dialog.save()
            if self.model.rowCount() > 0:
                self.model.removeRow(self.model.rowCount() - 1)
            self.model.appendRow((
                QtGui.QStandardItem(u'成功！')
            ))
            self.table.resizeColumnsToContents()  # 将列调整到跟内容大小相匹配
        dialog.destroy()

    def button_one_clicked(self):
        local_ip = socket.gethostbyname(socket.gethostname())
        # print "local ip:%s " % local_ip
        conf = ConfigParser.ConfigParser()
        conf.read(os.getcwd() + '/config/jdbc.cfg')
        conn = cx_Oracle.connect(conf.get('gz_oracle', 'username'),
                                 conf.get('gz_oracle', 'password'),
                                 conf.get('gz_oracle', 'server') + ':'
                                 + conf.get('gz_oracle', 'port') + '/'
                                 + conf.get('gz_oracle', 'sid'))
        cursor = conn.cursor()
        cursor.prepare("""select appid,ip from open_iplimit where ip = :ip""")
        cursor.execute(None, {'ip': local_ip})
        one = cursor.fetchone()
        if (one == None):
            param = {'ip': local_ip, 'appid': 'D9B14E43F0B993AEE040A8C0FB0174E7'}
            cursor.execute('insert into open_iplimit values(:appid,:ip)', param)
        cursor.close()
        conn.commit()
        conn.close()
        if self.model.rowCount() > 0:
            self.model.removeRow(self.model.rowCount() - 1)
        self.model.appendRow((
            QtGui.QStandardItem(u'IP插入成功！')
        ))
        self.table.resizeColumnsToContents()  # 将列调整到跟内容大小相匹配


    def create_war(self):
        dialog = file_dialog(parent=self)
        if dialog.exec_():
            # print dialog.source_dir()
            # print dialog.dest_dir()
            result = self.list_file(str(dialog.source_dir())+'/', str(dialog.dest_dir())+'/')
            if self.model.rowCount() > 0:
                self.model.removeRow(self.model.rowCount() - 1)
            self.model.appendRow((
                QtGui.QStandardItem(result)
            ))
            self.table.resizeColumnsToContents()  # 将列调整到跟内容大小相匹配
        dialog.destroy()


    def list_file(self, source_dir, target_dir):
        f = open("config/filelist.txt")
        line = f.readline()
        while line:
            self.copy_files(source_dir, target_dir, line.strip('\n'))
            line = f.readline()
        f.close()
        return u'成功'


    def copy_files(self, sourcedir, targetdir, file):
        source_file = os.path.join(sourcedir, file)
        target_file = os.path.join(targetdir, file)
        if not os.path.exists(targetdir + os.path.dirname(file)):
            os.makedirs(targetdir + os.path.dirname(file))
        if os.path.isfile(sourcedir + file):
            shutil.copyfile(source_file, target_file)

    def create_select(self, input_name, cursor):
        sql = 'select '
        while (1):
            row = cursor.fetchone()
            if row == None:
                break
            sql += row[0] + ','
        sql = sql[:-1]
        sql += ' from ' + input_name
        return sql


    def create_insert(self, input_name, cursor):
        sql = 'insert into ' + input_name + '('
        sql_value = ''
        while (1):
            row = cursor.fetchone()
            if row == None:
                break
            sql += row[0] + ','
            sql_value += ':' + row[0] + ','
        sql = sql[:-1]
        sql_value = sql_value[:-1]
        sql += ') values (' + sql_value + ')'
        return sql

    def create_update(self, input_name, cursor):
        sql = 'update ' + input_name + 'set '
        while (1):
            row = cursor.fetchone()
            if row == None:
                break
            sql += row[0] + '=:' + row[0] + ','
        sql = sql[:-1]
        return sql


def main():
    app = QtGui.QApplication(sys.argv)
    frame = Frame()
    frame.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()