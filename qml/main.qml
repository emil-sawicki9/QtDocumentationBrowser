import QtQuick.Window 2.2
import QtQuick 2.9
import QtQuick.Controls 2.9
import QtQuick.Layouts 1.15

import "components"
import "pages"

ApplicationWindow {
    id: root
    visible: true
    width: 600
    height: 400
    title: "Documentation viewer"
    flags: Qt.FramelessWindowHint | Qt.Window
    readonly property int delegateHeight: 30

    Rectangle {
        anchors.fill: parent
        color: "#0C0C0C"
    }

    Rectangle {
        id: topPanel
        anchors {
            left: parent.left
            right: parent.right
            top: parent.top
        }
        height: 20
        color: "#0C0C0C"

        MouseArea {
            property point previousPosition
            anchors.fill: parent
            onPressed: previousPosition = Qt.point(mouse.x, mouse.y)
            onPositionChanged: {
                root.setX(root.x + mouse.x - previousPosition.x)
                root.setY(root.y + mouse.y - previousPosition.y)
            }
        }

        Row {
            anchors {
                right: parent.right
                rightMargin: 5
                top: parent.top
                bottom: parent.bottom
            }

            layoutDirection: Qt.RightToLeft

            TopPanelButton {
                text: "-"
                onClicked: root.showMinimized()
            }

            TopPanelButton {
                text: "v"
                checkable: true
                onCheckedChanged: {
                    if (checked) {
                        root.flags |= Qt.WindowStaysOnTopHint
                    } else {
                        root.flags &= ~Qt.WindowStaysOnTopHint
                    }
                }
            }
        }
    }

    TabBar {
        id: tabBar
        anchors {
            top: topPanel.bottom
            left: parent.left
            right: parent.right
        }
        height: 40
        currentIndex: 0

        TabButton {
            text: "Frontpage"
        }
        TabButton {
            text: "Search"
        }
    }

    StackLayout {
        id: stackView
        anchors {
            left: parent.left
            right: parent.right
            top: tabBar.bottom
            bottom: parent.bottom
        }

        currentIndex: tabBar.currentIndex

        FrontPage {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        SearchPage {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }

}
