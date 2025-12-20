import QtQuick 2.5
import QtQuick.Window

Window {
    visible: true
    width: 640
    height: 480
    title: qsTr("Hello World")

    Rectangle {
        width: 100
        height: 100
        color: "red"

        Text {
            id: text
            text: "Hello World"
        }
    }
}