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
        function drawPixel(x, y, r, g, b, a, canvasData) {
            var index = (x + y * width) * 4;

            canvasData.data[index + 0] = r;
            canvasData.data[index + 1] = g;
            canvasData.data[index + 2] = b;
            canvasData.data[index + 3] = a;
        }
        function plotFun(fun, X){
            console.log(X, fun(X[2]));
            var ctx = getContext("2d");
            var canvasData = ctx.getImageData(0, 0, width, height);
            for (var i = 0; i < width; i++){
                drawPixel(i, 5, 0, 0, 0, 255, canvasData);
               
            }
            ctx.putImageData(canvasData, 0, 0);
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
            canvas.plotFun((function(x){return 2*x;}), [0,1,2,3,4,5,6,7,8,9,10]);
            canvas.requestPaint();
        }
    }
}
