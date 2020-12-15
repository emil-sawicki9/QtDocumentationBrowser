import QtQuick 2.0

Rectangle {
    id: root

    color: "transparent"
    border {
        width: 1
        color: "#3D3D3D"
    }

    property alias text: title.text
    property alias model: view.model

    signal openMenu(string url, int index, var delegate,real mouseX,real mouseY)

    Text {
        id: title
        anchors {
            top: parent.top
            left: parent.left
            margins: 5
        }
        color: "#CCCCCC"
        font.pixelSize: 13
    }

    ListView {
        id: view

        clip: true
        boundsBehavior: Flickable.StopAtBounds

        anchors {
            top: title.bottom
            topMargin: 10
            left: parent.left
            leftMargin: 2
            right: parent.right
            rightMargin: 5
            bottom: parent.bottom
            bottomMargin: 2
        }

        delegate: Rectangle {
            id: delegate
            property bool showHighlight: false
            color: delegateMA.containsMouse || showHighlight ? "#474747" : "#0C0C0C"
            width: view.width
            height: 25

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
                        app.open_in_external_browser(url)
                    } else {
                        root.openMenu(url, index, delegate, mouseX, mouseY)
                    }
                }
            }
        }

        ScrollBar {
            flickable: view
        }
    }
}
