import QtQuick 2.4
import QtQuick.Window 2.1
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.1
import QtQuick.Layouts 1.1

ApplicationWindow {
    title: "Billig"
    
    GridLayout {
        id: layout
        anchors.fill: parent

        Button{
            id: redraw
            objectName: "redraw"
            text : "Redraw"
            onClicked: {
                canvas.plotFun(pyfun.call, -5, 10, -10, 10, 100000);
            }
        }
    
        Canvas {
            id: canvas
            objectName: "canvas"
            antialiasing: true
            
            Layout.minimumWidth: 500
            Layout.minimumHeight: 500
            Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
            Layout.fillWidth: true
            Layout.fillHeight: true
            
            function drawAxes(xmin, xmax, ymin, ymax){
                var ctx = getContext("2d");
                ctx.reset();

                var x0 = xutop(0, xmin, xmax);
                var y0 = yutop(0, ymin, ymax);
                drawLine(x0, 0, x0, height);
                drawLine(0, y0, width, y0);
            }
            function xutop(x, xmin, xmax){
                // ppu = width/(xmax-xmin);
                return Math.round((x-xmin)*width/(xmax-xmin));
            }
            function yutop(y, ymin, ymax){
                // ppu = height/(ymax-ymin);
                return height-Math.round((y-ymin)*height/(ymax-ymin));
            }
            function drawLine(startx, starty, endx, endy){
                var ctx = getContext("2d");
                ctx.beginPath();
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
            function plot(X, Y, xmin, xmax, ymin, ymax){
                var ctx = getContext("2d");          
                var canvasData = ctx.getImageData(0, 0, width, height);
                for (var i = 0; i < X.length; i++){
                    drawPixel(xutop(X[i], xmin, xmax), yutop(Y[i], ymin, ymax), 0, 0, 0, 255, canvasData);
                }
                ctx.drawImage(canvasData, 0, 0);
                requestPaint();
            }
            function linspace(min, max, nval){
                var arr = new Array(nval);
                var step = (max-min)/nval;
                for (var i=0; i<nval; i++){
                    arr[i] = min + i*step;
                }
                return arr
            }
            function plotFun(fun, xmin, xmax, ymin, ymax, n){
                drawAxes(xmin, xmax, ymin, ymax)
                var X = linspace(xmin, xmax, n);
                var Y = X.map(fun)
                plot(X, Y, xmin, xmax, ymin, ymax);
                requestPaint();
            }
        }
    }

}
