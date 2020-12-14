import QtQuick 2.0

Rectangle {
    color: "transparent"
    border {
        width: 1
        color: "#3D3D3D"
    }

    property alias text: title.text
    property alias model: view.model

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
                    app.open_in_external_browser(url)
                }
            }
        }

        ScrollBar {
            flickable: view
        }
    }
}
