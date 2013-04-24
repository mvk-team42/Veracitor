var svg, info, circles, lines;
var time, run;
var mouse, mx, my, target;

var ns = "http://www.w3.org/2000/svg";

//var width = 800, height = 400;
var mass = 10, constraint = 8000, friction = 100, length = 200, pullforce = 10000;
var settle = 15, threshold = 0.00001, curlen, amount, update;

var FPS = 30;

window.onload = function () {
    var c, l, i, ltemp;

    svg = document.getElementById("svg");

    info = {
        "dom" : document.getElementById("info"),
        "ctx" : null,
        "width" : 200,
        "height" : 100,
        "data" : {},
        "lbound" : 0,
        "ubound" : 0,
        "max" : 0,
        "addData" : function (d) {
            if(this.max == 0) {
                this.lbound = this.ubound = d;
                } else {
                    if(d < this.lbound) {
                        this.lbound = d;
                        } else if(d > this.ubound) {
                            this.ubound = d;
                            }
                    }

            this.data[d] = (this.data[d])? this.data[d] + 1 : 1;

            if(this.data[d] > this.max) {
                this.max = this.data[d];
                }
            },
        "draw" : function () {
            var dx, dy, i;

            this.ctx.clearRect(0, 0, this.width, this.height);

            if(this.ubound - this.lbound == 0) {
                dx = this.width;
                } else {
                    dx = this.width / (this.ubound - this.lbound + 1);
                    }
            dy = (this.height - 15) / this.max;

            for(i = 0; i <= this.ubound - this.lbound; i ++) {
                if(this.data[this.lbound + i]) {
                    if(this.max == this.data[this.lbound + i]) {
                        this.ctx.fillStyle = "#000";

                        this.ctx.fillText("average " + (this.lbound + i) + " FPS", 0, this.height - 4);
                        } else {
                            this.ctx.fillStyle = "#aaa";
                            }

                    this.ctx.fillRect(
                        (i * dx) | 0, ((this.max - this.data[this.lbound + i]) * dy) | 0,
                        Math.ceil(dx), Math.ceil(this.data[this.lbound + i] * dy));
                    }
                }
            }
        };
    info.dom.width = info.width;
    info.dom.height = info.height;
    info.ctx = info.dom.getContext("2d");

    width = document.width;
    height = document.height - 10; // don't ask
    svg.setAttribute("width", width);
    svg.setAttribute("height", height);

    amount = 10;
    reset();

    document.addEventListener("keydown", keydown);
    document.addEventListener("mousedown", mousedown);
    document.addEventListener("mouseup", mouseup);
    document.addEventListener("mousemove", mousemove);
    document.addEventListener("mousewheel", mousewheel);

    if(window.requestAnimationFrame === null || typeof(window.requestAnimationFrame) === "undefined") {
        window.requestAnimationFrame = window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame || (function(callback, element) { return window.setTimeout(callback, 1000 / FPS); });
        }

    loop();
}

function loop () {
    var i;

    if(mouse) {
        circles[target].applyForce(pullforce * (mx - circles[target].getX()), pullforce * (my - circles[target].getY()));
        }

    for(i in circles) {
        circles[i].update();
        }

    for(i in lines) {
        lines[i].update();
        }

    time.cur = new Date().getTime();
    time.delta = (time.cur - time.prev) / 1000 % 1;
    time.prev = time.cur;

    //console.log(time.delta);
    if((update += time.delta) > 0.1) {
        //info.innerHTML = Math.round(1 / time.delta) + " (FPS)";
        info.addData(Math.round(1 / time.delta));
        info.draw();
        update = 0;
        }

    if(run) {
        window.requestAnimationFrame(loop);
        }
}

function reset () {
    circles = [];
    lines = [];
    curlen = length;

    for(i = 0; i < amount; i ++) {
        c = new Circle(Math.random()*(width - 100) + 50, Math.random()*(height - 100) + 50, (Math.random()*40 + 20) | 0);
        circles.push(c);
        }

    for(i = 0; i < circles.length; i ++) {
        if(i == circles.length - 1) {
            l = new Line(circles[i], circles[0], curlen);
            } else {
                l = new Line(circles[i], circles[i + 1], curlen);
                }
        lines.push(l);
        }

    for(i in lines) {
        svg.appendChild(lines[i].getDOM());
        }
    for(i in circles) {
        svg.appendChild(circles[i].getDOM());
        }

    time = {
        "cur" : 0,
        "prev" : new Date().getTime(),
        "delta" : 0
        };

    mouse = false;
    target = null;
    mx = 0; my = 0;
    update = 0;
    run = true;
}

function Circle (x, y, r) {
    var c = document.createElementNS(ns, "circle");
    var xv = 0,yv = 0,fx = 0,fy = 0;

    c.setAttributeNS(null, "cx", x);
    c.setAttributeNS(null, "cy", y);
    c.setAttributeNS(null, "r", r);
    c.setAttribute("style", "stroke: none; fill: rgb(" + (Math.random()*255 | 0) + "," + (Math.random()*255 | 0) + "," + (Math.random()*255 | 0) +");");

    this.getX = function () {
        return x;
        }

    this.getY = function () {
        return y;
        }

    this.getXV = function () {
        return xv;
        }

    this.getYV = function () {
        return yv;
        }

    this.setXY = function (nx, ny) {
        c.setAttributeNS(null, "cx", nx);
        c.setAttributeNS(null, "cy", ny);
        }

    this.getDOM = function () {
        return c;
        }

    this.applyForce = function (nfx, nfy) {
        fx += nfx;
        fy += nfy;
        }

    this.update = function () {
        if(xv > threshold) {
            xv -= xv * settle * time.delta;
            if(xv < 0) {
                xv = 0
                }
            } else if(xv < -threshold) {
                xv -= xv * settle * time.delta;
                if(xv > 0) {
                    xv = 0
                    }
                }
        if(yv > threshold) {
            yv -= yv * settle * time.delta;
            if(yv < 0) {
                yv = 0
                }
            } else if(yv < -threshold) {
                yv -= yv * settle * time.delta;
                if(yv > 0) {
                    yv = 0
                    }
                }

        xv += (fx / mass) * time.delta;
        yv += (fy / mass) * time.delta;

        fx = 0;
        fy = 0;

        x += xv * time.delta;
        y += yv * time.delta;

        this.setXY(x, y);
        }
}

function Line (c1, c2, len) {
    var l = document.createElementNS(ns, "line");
    l.setAttributeNS(null, "x1", c1.getX());
    l.setAttributeNS(null, "y1", c1.getY());
    l.setAttributeNS(null, "x2", c2.getX());
    l.setAttributeNS(null, "y2", c2.getY());
    l.setAttribute("style", "stroke: #666; stroke-width: 2px;");

    this.getDOM = function () {
        return l;
        }

    this.setLength = function (nl) {
        len = nl;
        }

    this.setCircles = function (nc1, nc2) {
        if(nc1 != null) {
            c1 = nc1;
            }
        if(nc2 != null) {
            c2 = nc2;
            }
        }

    this.update = function () {
        var fx, fy;
        var dx = c1.getX() - c2.getX();
        var dy = c1.getY() - c2.getY();
        var d = Math.sqrt(Math.pow(dx, 2) + Math.pow(dy, 2));

        if(d !== 0) {
            fx = -(dx / d) * (d - len) * constraint;
            fy = -(dy / d) * (d - len) * constraint;
            c1.applyForce(fx, fy);
            c2.applyForce(-fx, -fy);

            fx = -(c1.getXV() - c2.getXV()) * friction;
            fy = -(c1.getYV() - c2.getYV()) * friction;
            c1.applyForce(fx, fy);
            c2.applyForce(-fx, -fy);
            }

        l.setAttributeNS(null, "x1", c1.getX());
        l.setAttributeNS(null, "y1", c1.getY());
        l.setAttributeNS(null, "x2", c2.getX());
        l.setAttributeNS(null, "y2", c2.getY());
        }
}

/* KEYBOARD AND MOUSE INPUT */

function keydown (evt) {
    switch(evt.keyCode) {
        case 32:null
        var i;

        curlen = (curlen == 0)?length : 0;

        for(i in lines) {
            lines[i].setLength(curlen);
            }
        /*
          run = !run;

          if(run) {
          time.prev = new Date().getTime();
          loop();
          }
          */
        break;
        case 37:
        decrease();
        break;
        case 39:
        increase();
        break;
        }
}

function mousedown (evt) {
    var i, d, tmp;

    mouse = true;
    mx = evt.pageX;
    my = evt.pageY;

    d = Infinity;
    for(i in circles) {
        if((tmp = Math.sqrt(Math.pow(mx - circles[i].getX(), 2) + Math.pow(my - circles[i].getY(), 2))) < d) {
            d = tmp;
            target = i;
            }
        }

    circles[target].applyForce(pullforce * (mx - circles[target].getX()), pullforce * (my - circles[target].getY()));
};

function mouseup (evt) {
    mouse = false;
};

function mousemove (evt) {
    if(mouse) {
        mx = evt.pageX;
        my = evt.pageY;
        }
};

function mousewheel (evt) {
    if(evt.wheelDeltaY < 0) {
        decrease();
        } else {
            increase();
            }
}

function decrease () {
    if(!mouse) {
        amount --;

        if(amount < 2) {
            amount = 2;
            return;
            }

        svg.removeChild(circles.pop().getDOM());
        svg.removeChild(lines.pop().getDOM());

        lines[lines.length - 1].setCircles(null, circles[0]);
        }
}

function increase () {
    var c, l, x, y;

    if(!mouse) {
        amount ++;

        x = (circles[circles.length - 1].getX() - circles[0].getX()) / 2;
        x += (x < 0)? circles[0].getX() : circles[circles.length - 1].getX();

        y = (circles[circles.length - 1].getY() - circles[0].getY()) / 2;
        y += (y < 0)? circles[0].getY() : circles[circles.length - 1].getY();

        c = new Circle(x, y, (Math.random()*40 + 20) | 0);
        circles.push(c);
        lines[lines.length - 1].setCircles(null, c);
        l = new Line(c, circles[0], curlen);
        lines.push(l);

        svg.insertBefore(l.getDOM(), svg.firstChild);
        svg.appendChild(c.getDOM());
        }
}
