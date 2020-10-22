let c;
function setup(){
    let canv = createCanvas(200,200);
    canv.position(100,50)
    background(240);
}


function mouseDragged(){
    fill(0);
    circle(mouseX, mouseY, 30);

}
