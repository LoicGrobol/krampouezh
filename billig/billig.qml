import QtQuick 2.2
import QtQuick.Window 2.1
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.1

ApplicationWindow {
    title: qsTr("Test Invoke")
    
    Canvas {
        id: canvas
        width: 500
        height: 500
        
         onPaint: {
            var ctx = getContext("2d");
            ctx.reset();

            var centreX = width / 2;
            var centreY = height / 2;
            ctx.lineWidth = 1;

            ctx.beginPath();
            ctx.moveTo(centreX, 0);
            ctx.lineTo(centreX, height);
            ctx.moveTo(0, centreY);
            ctx.lineTo(width, centreY);
            ctx.stroke();

        }
    }

    //width: 200
    //height: 100

    Button{
      signal about_text
      objectName: "about_button"
      //y : 70
      text : "About"
      onClicked: {
	  about_text()
	  canvas.requestPaint()
      }
    }
}
