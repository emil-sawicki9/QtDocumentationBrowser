import QtQuick.Window 2.2
import QtQuick 2.9

import "table_view"

Window {
    visible: true
    width: 600
    height: 400
    title: "Documentation viewer"
    readonly property int delegateHeight: 30

    Rectangle {
        id: filterField
        anchors {
            top: parent.top
            left: parent.left
            leftMargin: 10
            rightMargin: 10
            right: parent.right
        }
        height: delegateHeight
        border {
            width: 1
            color: "black"
        }
        TextInput {
            id: filterInput
            anchors {
                fill: parent
                margins: 4
            }
            verticalAlignment: TextInput.AlignVCenter
            focus: true
            onTextChanged: documentationModel.filter(text)
            Text {
                anchors {
                    right: parent.right
                    rightMargin: 10
                    verticalCenter: parent.verticalCenter
                }
                visible: filterInput.text !== ""
                color: "black"
                text: "X"
            }
        }
        MouseArea {
            anchors {
                right: parent.right
                top: parent.top
                bottom: parent.bottom
            }
            width: 30
            enabled: filterInput.text !== ""
            onClicked: filterInput.text = ""
        }
    }

    DocumentationDelegate {
        id: listHeader
        anchors {
            top: filterField.bottom
            left: parent.left
            right: parent.right
        }
        height: delegateHeight
        textList: ["Name", "Type"]
        Rectangle {
            anchors.bottom: parent.bottom
            width: parent.width
            height: 1
            color: "black"
        }
    }

    ListView {
        id: documentationTable
        anchors {
            top: listHeader.bottom
            left: parent.left
            right: parent.right
            bottom: parent.bottom
        }
        clip: true
        boundsBehavior: Flickable.StopAtBounds
        model: documentationModel
        delegate: Rectangle {
            color: delegateMA.containsMouse ? "#30007CBA" : "white"
            width: documentationTable.width
            height: delegateHeight
            DocumentationDelegate {
                anchors.fill: parent
                textList: [name, description]
            }
            MouseArea {
                id: delegateMA
                anchors.fill: parent
                hoverEnabled: true
                onClicked: Qt.openUrlExternally(url)
            }
        }
        Rectangle {
            anchors {
                top: parent.top
                right: parent.right
                bottom: parent.bottom
            }
            visible: documentationTable.visibleArea.heightRatio !== 1
            enabled: visible
            color: scrollbarMA.containsMouse ? "#20808080" : "transparent"
            width: scrollbarMA.containsMouse ? 15 : 5
            Behavior on width {
                NumberAnimation { duration: 100 }
            }
            Rectangle {
                id: scrollbarRect
                anchors {
                    right: parent.right
                }
                y: documentationTable.visibleArea.yPosition * documentationTable.height
                width: parent.width
                height: Math.max(10, documentationTable.visibleArea.heightRatio * documentationTable.height)
                color: "#AA808080"
            }
            MouseArea {
                id: scrollbarMA
                anchors.fill: parent
                hoverEnabled: true
                preventStealing: true
                property bool draggingScrollbar: false
                function updatePosition() {
                    var yPos = Math.max(0, mouseY)
                    if ( yPos >= scrollbarMA.height) {
                        documentationTable.contentY = documentationTable.contentHeight - documentationTable.height
                    } else {
                        documentationTable.contentY = yPos / scrollbarMA.height * documentationTable.contentHeight
                    }
                }
                onPressed: {
                    if ( mouseY >= scrollbarRect.y && mouseY <= (scrollbarRect.height + scrollbarRect.y) ) {
                        draggingScrollbar = true
                    } else {
                        updatePosition()
                    }
                }
                onReleased: draggingScrollbar = false
                onPositionChanged: {
                    if ( draggingScrollbar ) {
                        updatePosition()
                    }
                }
            }
        }
    }

}