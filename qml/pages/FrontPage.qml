import QtQuick 2.0
import QtQuick.Layouts 1.10

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
        }

        DocumentationPinnedList {
            Layout.fillWidth: true
            Layout.fillHeight: true
            text: "Most used"
            model: mostUsedModel
        }
    }
}
