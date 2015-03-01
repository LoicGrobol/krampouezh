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
                canvas.setWindow(-5,10,-10,10);
                canvas.plotFun(pyfun.call, 100000);
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
            
            property int xmin
            property int xmax
            property int ymin
            property int ymax
            xmin: -10
            xmax: 10
            ymin: -10
            ymax: 10
            
            function drawAxes(){
                var ctx = getContext("2d");
                ctx.reset();

                var x0 = xutop(0);
                var y0 = yutop(0);
                drawLine(x0, 0, x0, height);
                drawLine(0, y0, width, y0);
            }
            function xutop(x){
                // Conversion from plto window-relative coordinate to canvas pixel coordinates (x axis)
                // ppu = width/(xmax-xmin);
                return Math.round((x-xmin)*width/(xmax-xmin));
            }
            function yutop(y){
                // Conversion from plto window-relative coordinate to canvas pixel coordinates (y axis)
                // ppu = height/(ymax-ymin);
                return height-Math.round((y-ymin)*height/(ymax-ymin));
            }
            function drawLine(startx, starty, endx, endy){
                // Uses canvas pixel coordinates
                var ctx = getContext("2d");
                ctx.beginPath();
                ctx.moveTo(startx, starty),
                ctx.lineTo(endx, endy);
                ctx.stroke();
            }
            function drawPixel(x, y, r, g, b, a, canvasData) {
                // Uses canvas pixel coordinates
                var index = (x + y * width) * 4;

                canvasData.data[index + 0] = r;
                canvasData.data[index + 1] = g;
                canvasData.data[index + 2] = b;
                canvasData.data[index + 3] = a;
            }
            function plot(X, Y){
                var ctx = getContext("2d");          
                var canvasData = ctx.getImageData(0, 0, width, height);
                for (var i = 0; i < X.length; i++){
                    drawPixel(xutop(X[i]), yutop(Y[i]), 0, 0, 0, 255, canvasData);
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
            function plotFun(fun, n){
                drawAxes(xmin, xmax, ymin, ymax)
                var X = linspace(xmin, xmax, n);
                var Y = X.map(fun)
                plot(X, Y);
                requestPaint();
            }
            function setWindow(xmn, xmx, ymn, ymx){
                xmin = xmn;
                xmax = xmx;
                ymin = ymn;
                ymax = ymx;
            }
            
        }
    }

}
