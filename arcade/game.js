(() => {
const canvas=document.querySelector("#game"),ctx=canvas.getContext("2d");
const scoreEl=document.querySelector("#score"),bestEl=document.querySelector("#best"),statusEl=document.querySelector("#status");
const overlay=document.querySelector("#overlay"),titleEl=document.querySelector("#overlayTitle"),textEl=document.querySelector("#overlayText"),startBtn=document.querySelector("#start");
const CELL=20,COLS=canvas.width/CELL,ROWS=canvas.height/CELL;
let snake,food,dir,nextDir,score,best=0,timer,running=false,paused=false;
try{best=Number(localStorage.getItem("s0k1x-cybersnake-best")||0)}catch{}
bestEl.textContent=String(best).padStart(4,"0");
function reset(){snake=[{x:8,y:10},{x:7,y:10},{x:6,y:10}];dir={x:1,y:0};nextDir={...dir};score=0;scoreEl.textContent="0000";spawnFood();draw()}
function spawnFood(){do{food={x:Math.floor(Math.random()*COLS),y:Math.floor(Math.random()*ROWS)}}while(snake.some(p=>p.x===food.x&&p.y===food.y))}
function draw(){ctx.fillStyle="#05030a";ctx.fillRect(0,0,canvas.width,canvas.height);ctx.strokeStyle="#171026";
for(let x=0;x<=canvas.width;x+=CELL){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,canvas.height);ctx.stroke()}
for(let y=0;y<=canvas.height;y+=CELL){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(canvas.width,y);ctx.stroke()}
ctx.shadowBlur=16;ctx.shadowColor="#ff00a8";ctx.fillStyle="#ff00a8";ctx.fillRect(food.x*CELL+4,food.y*CELL+4,CELL-8,CELL-8);
snake.forEach((p,i)=>{ctx.fillStyle=i===0?"#00ff88":"#00cbd8";ctx.shadowColor=i===0?"#00ff88":"#00f5ff";ctx.fillRect(p.x*CELL+2,p.y*CELL+2,CELL-4,CELL-4)});ctx.shadowBlur=0}
function end(){running=false;clearTimeout(timer);statusEl.textContent="OFFLINE";titleEl.textContent="SIGNAL LOST";textEl.textContent=`Score: ${score}. Reboot and try again.`;startBtn.textContent="RETRY";overlay.classList.remove("hidden")}
function tick(){if(!running||paused)return;dir=nextDir;const head={x:snake[0].x+dir.x,y:snake[0].y+dir.y};
if(head.x<0||head.x>=COLS||head.y<0||head.y>=ROWS||snake.some(p=>p.x===head.x&&p.y===head.y)){end();return}
snake.unshift(head);if(head.x===food.x&&head.y===food.y){score+=10;scoreEl.textContent=String(score).padStart(4,"0");if(score>best){best=score;bestEl.textContent=String(best).padStart(4,"0");try{localStorage.setItem("s0k1x-cybersnake-best",String(best))}catch{}}spawnFood()}else snake.pop();draw();timer=setTimeout(tick,Math.max(65,135-score/5))}
function start(){clearTimeout(timer);reset();running=true;paused=false;statusEl.textContent="ONLINE";overlay.classList.add("hidden");tick()}
function change(d){const map={up:{x:0,y:-1},down:{x:0,y:1},left:{x:-1,y:0},right:{x:1,y:0}},n=map[d];if(!n||n.x===-dir.x&&n.y===-dir.y)return;nextDir=n}
document.addEventListener("keydown",e=>{const keys={ArrowUp:"up",w:"up",ArrowDown:"down",s:"down",ArrowLeft:"left",a:"left",ArrowRight:"right",d:"right"};if(keys[e.key]){e.preventDefault();change(keys[e.key])}if(e.key.toLowerCase()==="p"&&running){paused=!paused;statusEl.textContent=paused?"PAUSED":"ONLINE";if(!paused)tick();else clearTimeout(timer)}if(e.key==="Enter"&&!running)start()});
document.querySelectorAll("[data-dir]").forEach(b=>b.addEventListener("click",()=>change(b.dataset.dir)));startBtn.addEventListener("click",start);reset();
})();
