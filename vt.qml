import QtQuick 2.5
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.3

ApplicationWindow {
    title: "ValueTracker"
    visible: true
    minimumHeight: 600
    minimumWidth: 800
    statusBar: StatusBar {
        RowLayout {
            anchors.fill: parent
            Label { text: "Read Only" }
        }
    }
    menuBar: MenuBar {
        Menu {
            title: "File"
            MenuItem { text: "Open..." }
            MenuItem { text: "Close" }
        }

        Menu {
            title: "Edit"
            MenuItem { text: "Cut" }
            MenuItem { text: "Copy" }
            MenuItem { text: "Paste" }
        }
    }
}