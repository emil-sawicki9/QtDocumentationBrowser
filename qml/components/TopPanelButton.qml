import QtQuick 2.0

Rectangle {
    id: root

    property alias text: buttonText.text
    property bool checkable: false
    property bool checked: false

    signal clicked

    anchors {
        top: parent.top
        bottom: parent.bottom
        margins: 3
    }

    color: ma.containsMouse || root.checked ? "#80808080" : "transparent"
    width: 20

    Text {
        id: buttonText
        anchors.centerIn: parent
        color: "white"
        font.pixelSize: 20
    }

    MouseArea {
        id: ma
        anchors.fill: parent
        hoverEnabled: true
        onClicked: {
            if (checkable) {
                root.checked = !root.checked
            }
            root.clicked()
        }
    }
}