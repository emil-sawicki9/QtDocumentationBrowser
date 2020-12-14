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
        property bool isPinned: false
        modal: true
        dim: false
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
        Action {
            text: "Upin item"
            onTriggered: app.pin_item(pinnedMenu.url, false)
        }
    }
}
