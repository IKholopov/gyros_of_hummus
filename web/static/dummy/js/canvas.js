var canvas = document.getElementById("background");
var context = canvas.getContext("2d");
W = window.innerWidth;
H = window.innerHeight;
var particles = {};
var N = 10;
var batches = 5;
var added_particles = 0;
var v = 13;
function initCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    context.fillStyle = "rgba(23, 13, 38, 1)";
    context.fillRect(0,0, canvas.width, canvas.height);
}

function addParticles() {
        var i = 0;
    for(i = added_particles; i < added_particles + N; ++i) {
        particles[i] = {
            angle: Math.PI * i*1./N/batches - Math.PI / 2,
            x: (Math.random() - 0.5) * W / 10  + W/2,
            y: (Math.random() - 0.5) * H / 10 + H/2
        }
    }
    for(i = added_particles + N; i < added_particles + 2*N; ++i) {
        particles[i] = {
            angle: Math.PI * i*1./N/batches - Math.PI/2,
            x: (Math.random() - 0.5) * W / 10  + W/2,
            y: (Math.random() - 0.5) * H / 10 + H/2
        }
    }
    added_particles += 2*N;
}

function drawParticle(x, y, size) {
    context.fillStyle = "white";
    context.fillRect(x, y, size, size);
}
initCanvas();
setInterval(function() {
    // Erase canvas
        context.fillStyle = "black";
        context.fillRect(0, 0, W, H);

        for(var i = 0; i < added_particles; ++i) {
            particles[i].x += v*Math.cos(particles[i].angle);
            particles[i].y += v*Math.sin(particles[i].angle);
            var x = particles[i].x;
            var y = particles[i].y;
            if(x > W || x < 0 ||
                y > H || y < 0) {
                particles[i].x = (Math.random() - 0.5) * W / 50  + W/2;
                particles[i].y = (Math.random()-0.5) * H / 50 + H/2;
                particles[i].angle = Math.random()*2*Math.PI;
            }
            x = particles[i].x;
            y = particles[i].y;
            drawParticle(particles[i].x, particles[i].y, Math.min(Math.sqrt((x-W/2)*(x-W/2)+(y-H/2)*(y-H/2))/100, 2));
        }

      }, 30);
for(var j = 0; j < batches; ++j) {
    setTimeout(addParticles, 500*j);
}



