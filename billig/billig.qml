import QtQuick 2.2
import QtQuick.Window 2.1
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.1

ApplicationWindow {
    title: qsTr("Test Invoke")

    //width: 200
    //height: 100

    Button{
      signal about_text
      objectName: "about_button"
      //y : 70
      text : "About"
      onClicked: {
	  about_text()
      }
    }
}
