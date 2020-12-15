import QtQuick 2.0
import QtQuick.Layouts 1.10
import QtQuick.Controls 2.9

import "../components"

Item {
    GridLayout {
        anchors {
            fill: parent
            margins: 10
        }
        rows: 2
        columns: 2

        DocumentationPinnedList {
            Layout.fillWidth: true
            Layout.fillHeight: true
            text: "Latest"
            model: latestModel
        }

        DocumentationPinnedList {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.rowSpan: 2
            text: "Pinned"
            model: pinnedModel
            onOpenMenu: {
                pinnedMenu.url = url
                pinnedMenu.index = index
                pinnedMenu.popup(delegate, mouseX, mouseY)
            }
        }

        DocumentationPinnedList {
            Layout.fillWidth: true
            Layout.fillHeight: true
            text: "Most used"
            model: mostUsedModel
        }
    }

    Menu {
        id: pinnedMenu
        property var url: ""
        property int index: -1
        property bool isPinned: false
        modal: true
        dim: false
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
        Action {
            text: "Move up"
            enabled: pinnedMenu.index > 0
            onTriggered: app.move_pin_item(pinnedMenu.url, true)
        }
        Action {
            text: "Move down"
            enabled: pinnedMenu.index < pinnedModel.rowCount() - 1
            onTriggered: app.move_pin_item(pinnedMenu.url, false)
        }
        Action {
            text: "Upin item"
            onTriggered: app.pin_item(pinnedMenu.url, false)
        }
    }
}
