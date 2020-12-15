import QtQuick 2.9

Rectangle {

    property var flickable

    anchors {
        top: parent.top
        right: parent.right
        bottom: parent.bottom
    }

    visible: flickable.visibleArea.heightRatio !== 1
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
        y: flickable.visibleArea.yPosition * flickable.height
        width: parent.width
        height: Math.max(10, flickable.visibleArea.heightRatio * flickable.height)
        radius: 4
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
                flickable.contentY = flickable.contentHeight - flickable.height
            } else {
                flickable.contentY = yPos / scrollbarMA.height * flickable.contentHeight
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
