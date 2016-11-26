/**
 * Created by igor on 11/26/16.
 */
var grid = {};
var marker = "blue";
    function previewFile(){
       var preview = document.querySelector('img'); //selects the query named img
       var file    = document.querySelector('input[type=file]').files[0]; //sames as here
       var reader  = new FileReader();

       reader.onloadend = function () {
           preview.src = reader.result;
       }

       if (file) {
           reader.readAsDataURL(file); //reads the data as a URL
       } else {
           preview.src = "";
       }


    }
    function switchMarker(mark) {
        if(mark == 0)
            marker = "red";
        if(mark == 1)
            marker = "blue";
        if(mark == 2)
            marker = "yellow";
    }
    function renderGrid() {
        for(var i = 0; i < grid.size; ++i)  {
            for(var j = 0; j < grid[i].size; ++j) {
                document.getElementById(String(i) + "_" + String(j)).parentElement.removeChild(grid[i][j]);
            }
        }
        var width = document.getElementById("image").width;
        var height = document.getElementById("image").height;
        document.getElementById("paint").width = width;
        document.getElementById("paint").height = height;
        var x_res = document.getElementById("width").value;

        var y_res = document.getElementById("height").value;
        if(x_res < 1 || y_res < 1)
            return;
        for(var i = 0; i < x_res; ++i) {
            grid[i] = {};
            for(var j = 0; j < y_res; ++j) {
                var point = document.createElement("a");
                point.id = String(i) + "_" + String(j);
                document.getElementById("paint").appendChild(point)
                point = document.getElementById(String(i) + "_" + String(j));
                point.style.width = width/x_res/2+"px";
                point.style.height = height/y_res/2+"px";
                point.style.position = "absolute";
                point.style.left = i * width / x_res + "px";
                point.style.top = j * height / y_res + "px";
                point.style.backgroundColor=marker;
                point.addEventListener(
                    "click",
                    function(e){
                        e.target.style.backgroundColor = marker;
                    },
                    false);
                grid[i][j] = point;
            }
        }
    }
    function sendmap() {
        if(grid.size == 0) {
            alert("Empty grid!");
            return;
        }
        var title = document.getElementById("title").value;
        return $.post("/maplayer/", {
            title:title,

        });
    }

