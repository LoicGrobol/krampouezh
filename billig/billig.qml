import QtQuick 2.4
import QtQuick.Window 2.1
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.1

ApplicationWindow {
    title: "Billig"
    
    Canvas {
        id: canvas
        objectName: "canvas"
        width: 500
        height: 500
        
        function drawAxes(){
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
        function drawLine(startx, starty, endx, endy){
            var ctx = getContext("2d");
            ctx.moveTo(startx, starty),
            ctx.lineTo(endx, endy);
            ctx.stroke();
        }
        onPaint: {
            drawAxes();
        }
    }

    Button{
      id: redraw
      objectName: "redraw"
      text : "Redraw"
      onClicked: {

	  canvas.requestPaint()
      }
    }
}
