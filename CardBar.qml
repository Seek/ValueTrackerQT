import QtQuick 2.5
import QtQuick.Controls 1.2
import QtQuick.Layouts 1.3

Rectangle {
    // Basic properties
    id: cardBar
    property string cardId
    property string cardName
    property int cardCost
    property int numCards
    
    // Style
    color: "#636363"
    width: parent.width
    height: 35
    state: "NORMAL_NUM"
    radius: 3
    antialiasing: true

    onCardIdChanged: cardImage.source = 'images/bars/'.concat(cardId).concat('.png')
    //onCardNameChanged
    //onCardCostChanged
    //onNumCardsChanged
    // Card Image
    Image {
        id: cardImage
        fillMode: Image.PreserveAspectCrop
        source: 'images/bars/AT_001.png'
        anchors.right: parent.right
    }
    // Cost
    Rectangle {
        id: costRect
        antialiasing: parent.antialiasing
        color: "#8C8C8C"
        width: 35
        height: parent.height
        border.width: 1
        border.color: "black"
        radius: parent.radius
        anchors.left: parent.left
        Text {
            id: costText
            style: Text.Outline; styleColor: "black"
            text: "6"
            font.pointSize: 18
            anchors.centerIn: parent
        }
    }
    // Num cards
    // Cost
    Rectangle {
        id: numRect
        antialiasing: parent.antialiasing
        color: "#8C8C8C"
        width: 35
        height: parent.height
        border.width: 1
        border.color: "black"
        radius: parent.radius
        anchors.right: parent.right
        Text {
            id: numText
            style: Text.Outline; styleColor: "black"
            text: "6"
            color: "yellow"
            font.pointSize: 18
            anchors.centerIn: parent
        }
    }
    // Name text
    Text {
        id: nameText
        style: Text.Outline; styleColor: "black"
        text: "Polymorph"
        font.pointSize: 16
        anchors.left: costRect.right
        anchors.verticalCenter: parent.verticalCenter
        anchors.leftMargin: 5
    }

    // States
    states: [
        State {
            name: "NORMAL_NUM"
            PropertyChanges { target: costText; color: "white"}
            PropertyChanges { target: nameText; color: "white"}
            AnchorChanges { target:cardImage; anchors.right: numRect.left}
            PropertyChanges { target: numRect; opacity: 1}
        },
        State {
            name: "NORMAL_NONUM"
            PropertyChanges { target: costText; color: "white"}
            PropertyChanges { target: nameText; color: "white"}
            AnchorChanges { target:cardImage; anchors.right: cardBar.right}
            PropertyChanges { target: numRect; opacity: 0}
        },
        State {
            name: "DRAWN"
            PropertyChanges { target: costText; color: "green"}
        },
        State {
            name: "FATIGUED"
            PropertyChanges { target: cardBar; color: "black"}
            PropertyChanges { target: costText; color: "white"}
            PropertyChanges { target: nameText; color: "white"}
        }
    ]
    transitions: [
        Transition {
            from: "NORMAL_NUM"
            to: "NORMAL_NONUM"
            PropertyAnimation {target: numRect; properties: "opacity"; to: "0"; duration: 250; easing.type: Easing.OutCubic}
            AnchorAnimation { duration: 1000; easing.type: Easing.OutBounce }
        },
        Transition {
            from: "NORMAL_NONUM"
            to: "NORMAL_NUM"
            PropertyAnimation {target: numRect; properties: "opacity"; to: "1"; duration: 250; easing.type: Easing.OutCubic}
            AnchorAnimation { duration: 200; easing.type: Easing.OutQuad }
        }
    ]
}