import QtQuick 2.9
import QtQuick.Controls 2.9
import QtQuick.Dialogs 1.3

import "../components"

Item {
    Rectangle {
        id: filterField
        anchors {
            top: parent.top
            topMargin: 10
            left: parent.left
            leftMargin: 10
            rightMargin: 10
            right: parent.right
        }
        height: delegateHeight
        color: "#7F7F7F"
        border {
            width: 1
            color: "white"
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
            color: "white"
            selectByMouse: true

            Text {
                anchors {
                    right: parent.right
                    rightMargin: 10
                    verticalCenter: parent.verticalCenter
                }
                visible: filterInput.text !== ""
                color: "white"
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

    Row {
        id: typeSelectRow
        anchors {
            top: filterField.bottom
            topMargin: 10
            left: parent.left
            leftMargin: 20
        }

        height: 30
        spacing: 10

        Text {
            anchors.verticalCenter: parent.verticalCenter
            text: "Choose type:"
            color: "white"
        }

        ComboBox {
            anchors.verticalCenter: parent.verticalCenter
            model: ["All", "Qt", "QML"]
            height: parent.height * 0.75

            onCurrentIndexChanged: documentationModel.filter_by_type(currentIndex)
        }

    }

    DocumentationDelegate {
        id: listHeader
        anchors {
            top: typeSelectRow.bottom
            left: parent.left
            right: parent.right
        }
        height: delegateHeight
        textList: ["Name", "Type"]

        Rectangle {
            anchors.bottom: parent.bottom
            width: parent.width
            height: 1
            color: "#0C0C0C"
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
        enabled: !delegateMenu.visible
        delegate: Rectangle {
            id: delegate
            property bool showHighlight: false
            color: delegateMA.containsMouse || showHighlight ? "#474747" : "#0C0C0C"
            width: documentationTable.width
            height: delegateHeight

            Connections {
                target: delegateMenu
                function onClosed() {
                    delegate.showHighlight = false
                }
            }

            DocumentationDelegate {
                anchors.fill: parent
                textList: [name, description]
            }

            MouseArea {
                id: delegateMA
                anchors.fill: parent
                hoverEnabled: true
                acceptedButtons: Qt.LeftButton | Qt.RightButton
                onClicked: {
                    if ( mouse.button === Qt.LeftButton ) {
//                        app.open_new_tab(url)
                        app.open_in_external_browser(url)
                    } else {
                        delegate.showHighlight = true
                        delegateMenu.url = url
                        delegateMenu.isPinned = isPinned
                        delegateMenu.popup(delegate, mouseX, mouseY)
                    }
                }
            }
        }

        ScrollBar {
            flickable: documentationTable
        }
    }

    Rectangle {
        anchors {
            left: parent.left
            right: parent.right
            top: documentationTable.top
        }
        height: 1
        color: "white"
    }

    Menu {
        id: delegateMenu
        property var url: ""
        property bool isPinned: false
        modal: true
        dim: false
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
        onClosed: filterInput.forceActiveFocus()
        Action {
            text: "Open in new tab"
            onTriggered: {

            }
        }
        Action {
            text: "Open in external browser"
            onTriggered: app.open_in_external_browser(delegateMenu.url)
        }
        Action {
            text: "Pin to frontpage"
            onTriggered: messageDialog.open()
        }
        Action {
            text: delegateMenu.isPinned ? "Upin item" : "Pin item"
            onTriggered: app.pin_item(delegateMenu.url, !delegateMenu.isPinned)
        }
    }

    MessageDialog {
        id: messageDialog
        title: "Error"
        text: "Not implemented yet."
    }
}
