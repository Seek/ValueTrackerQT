import QtQuick 2.5
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.3
import TrackedCards 1.0


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

    ColumnLayout {
        width: 250
        height: 600
        anchors.horizontalCenter: parent.horizontalCenter
        CardBar {id: bar; cardId: "AT_002"}
    }
    ColumnLayout {
        Button {
            text: "Forward"
            onClicked: bar.state = "NORMAL_NONUM"
        }
        Button {
            text: "Back"
            onClicked: bar.state = "NORMAL_NUM"
        }
    }
    TrackedCard {
        objectName: "card"
        onCardsChanged: console.log("We got", cards['dd'] )
    }
    Rectangle {
        width: 180; height: 200
        objectName: "myList"
        
        function append(newElement) {
            contactModel.append(newElement)
        }
        
        Component {
            id: contactDelegate
            Item {
                width: 180; height: 40
                CardBar {}
            }
        }
        ListView {
            id: myId
            anchors.fill: parent
            model: pythonList
            delegate: contactDelegate
            highlight: Rectangle { color: "lightsteelblue"; radius: 5 }
            focus: true
        }
    }

    TextField {
        objectName: "autoComplete"
        signal textModified(string text)
        
        anchors.centerIn: parent
        inputMethodHints: Qt.ImhNoPredictiveText
        onTextChanged: {
            console.log("Text changed to:", text)
            textModified(text)
        }
    }

}