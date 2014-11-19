# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './populate_credentials_dialog_base.ui'
#
# Created: Wed Nov 19 13:02:17 2014
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PopulateCredentialsDialogBase(object):
    def setupUi(self, PopulateCredentialsDialogBase):
        PopulateCredentialsDialogBase.setObjectName(_fromUtf8("PopulateCredentialsDialogBase"))
        PopulateCredentialsDialogBase.resize(400, 300)
        self.button_box = QtGui.QDialogButtonBox(PopulateCredentialsDialogBase)
        self.button_box.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName(_fromUtf8("button_box"))

        self.retranslateUi(PopulateCredentialsDialogBase)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), PopulateCredentialsDialogBase.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), PopulateCredentialsDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(PopulateCredentialsDialogBase)

    def retranslateUi(self, PopulateCredentialsDialogBase):
        PopulateCredentialsDialogBase.setWindowTitle(_translate("PopulateCredentialsDialogBase", "Populate Credentials", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PopulateCredentialsDialogBase = QtGui.QDialog()
    ui = Ui_PopulateCredentialsDialogBase()
    ui.setupUi(PopulateCredentialsDialogBase)
    PopulateCredentialsDialogBase.show()
    sys.exit(app.exec_())

