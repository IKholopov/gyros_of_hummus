/**
 * Created by igor on 11/26/16.
 */
var grid = [];
var floor_grid = [];
var color_red = "rgba(256,0,0,0.5)";
var color_yellow = "rgba(170,170,0,0.5)";
var color_green = "rgba(0,256,0,0.5)";
var color_blue = "rgba(0,0,256,0.5)";
var marker = 0;
var offices = [];

$('document').ready(function() {document.getElementById("office_name").style.display="none";})

function add_office(coord) {
    var name = document.getElementById("office_name").value;
    offices[offices.length] = {
        name: name,
        coords: coord
    }
    var node = document.createElement("p");
    var text = document.createTextNode(name);
    node.appendChild(text);
    document.getElementById("office_list").appendChild(node);
}

function colorForMarker() {
    if(marker == 0)
        return color_blue;
    if(marker == 1)
        return color_red;
    if(marker == 2)
        return color_yellow;
}
    function previewFile(){
        document.getElementById("blanket").style.display = "none";
        var preview = document.querySelector('img'); //selects the query named img
        var file    = document.querySelector('input[type=file]').files[0]; //sames as here
        var reader  = new FileReader();
        reader.onloadend = function () {
                preview.src = reader.result;
                renderGrid();
        }

        if (file) {
            reader.readAsDataURL(file); //reads the data as a URL
        } else {
            preview.src = "";
        }

    }
    function switchMarker(mark) {
        console.log(mark);
        if(mark == 3) {
            document.getElementById("office_name").style.display = "";
        }
        else {
            document.getElementById("office_name").style.display = "none";
        }
        marker = mark;
    }
    function renderGrid() {
        switchMarker(0);
        offices = [];
        for(var i = 0; i < grid.length; ++i)  {
            for(var j = 0; j < grid[i].length; ++j) {
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
            grid[i] = [];
            floor_grid[i] = [];
            for(var j = 0; j < y_res; ++j) {
                var point = document.createElement("a");
                point.id = String(i) + "_" + String(j);
                document.getElementById("paint").appendChild(point)
                point = document.getElementById(String(i) + "_" + String(j));
                point.style.width = width/x_res+"px";
                point.style.height = height/y_res+"px";
                point.style.position = "absolute";
                point.style.left = i * width / x_res + "px";
                point.style.top = j * height / y_res + "px";
                point.style.backgroundColor=colorForMarker();
                floor_grid[i][j] = marker;
                point.addEventListener(
                    "mouseover",
                    function(e){
                        if(marker == 3)
                            return;
                        if(e.buttons == 1 || e.buttons == 3) {
                            e.target.style.backgroundColor = colorForMarker();
                        }
                        var cord = e.target.id.split('_');
                        floor_grid[cord[0]][cord[1]] = marker;
                    },
                    false);
                point.addEventListener(
                    "click",
                    function(e){
                        if(marker == 3) {
                            var cord = e.target.id.split('_');
                            add_office(cord);
                            e.target.style.backgroundColor = color_green;
                            return;
                        }
                        e.target.style.backgroundColor = colorForMarker();
                        var cord = e.target.id.split('_');
                        floor_grid[cord[0]][cord[1]] = marker;
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
        var floor = document.getElementById("floor").value;
        var a_x = document.getElementById("a_x").value;
        var a_y = document.getElementById("a_y").value;
        var b_x = document.getElementById("b_x").value;
        var b_y = document.getElementById("b_y").value;
        $.post("/maplayer/", {
            title:title,
            floor: floor,
            field: JSON.stringify(floor_grid),
            a_align_x: a_x,
            a_align_y: a_y,
            b_align_x: b_x,
            b_align_y: b_y
        });
        offices_to_send = []
        for(var i = 0; i < offices.length; ++i)
            $.post("/office/", {
                name:offices[i].name,
                x_coord: offices[i].coords[0],
                y_coord: offices[i].coords[1],
                floor: floor
        });
    }

    function test1() {

}
function test() {
    alert("test");
}