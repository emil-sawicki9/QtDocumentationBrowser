import sys

from PyQt5.QtCore import QCoreApplication
from tendo import singleton

from PyQt5 import QtCore

from documentation_processing.application import Application


def qt_message_handler(mode, context, message):
    if mode == QtCore.QtInfoMsg:
        mode = 'Info'
    elif mode == QtCore.QtWarningMsg:
        mode = 'Warning'
    elif mode == QtCore.QtCriticalMsg:
        mode = 'critical'
    elif mode == QtCore.QtFatalMsg:
        mode = 'fatal'
    else:
        mode = 'Debug'
    print("%s: %s (%s:%d, %s)" % (mode, message, context.file, context.line, context.file))


if __name__ == '__main__':
    me = singleton.SingleInstance()
    QtCore.qInstallMessageHandler(qt_message_handler)
    QCoreApplication.setOrganizationName("LidoSoft");
    QCoreApplication.setApplicationName("QtDocumentationViewer");
    app = Application(sys.argv)
    sys.exit(app.exec_())
