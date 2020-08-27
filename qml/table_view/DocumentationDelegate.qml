import QtQuick 2.3

Item {
    width: parent.width

    property var textList: ["", ""]

    Text {
        anchors.centerIn: parent
        anchors.horizontalCenterOffset: -parent.width * 0.25
        text: textList[0]
    }

    Rectangle {
        anchors.centerIn: parent
        width: 1
        height: parent.height
        color: "black"
    }

    Text {
        anchors.centerIn: parent
        anchors.horizontalCenterOffset: parent.width * 0.25
        text: textList[1]
    }
}