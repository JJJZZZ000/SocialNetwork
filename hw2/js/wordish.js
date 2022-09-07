var target;
var row_idx = 0;
var target_dic = {}
var rows = document.getElementsByTagName("tr");
function start(){
    row_idx = 0;
    target = "";
    target_dic = {}
    rows = document.getElementsByTagName("tr");

    status_change("Welcome to Wordish");
    target = document.getElementById("target_text").value;
    if(!isValidWord(target)){
        status_change("Invalid target");
    }
    var cells = document.getElementsByTagName("td");
    for(let i = 0; i < cells.length; i++){
        var cell = cells[i];
        cell.innerText = null;
    }
    for(let i = 0; i < target.length; i++){
        var ch = target.charAt(i);
        if(target_dic[ch] == null){
            target_dic[ch] = 0;
        }
        target_dic[ch] = target_dic[ch]+1;
    }
    status_change("start");
}
function isValidWord(word){
    if(word.length !== 5) return false;
    for(let i = 0; i < 5; i++){
        var ch = word.charAt(i);
        if(!((ch >= 'a' && ch <= 'z') || (ch >='A' && ch <='Z'))) return false;
    }
    return true;
}
function status_change(msg){
    var status = document.getElementById("status");
    status.innerHTML = msg;
}
function submit(){
    var guess = document.getElementById("guess_text").value;
    if(target == null){
        status_change("Invalid target");
        return;
    }
    if(!isValidWord(guess)){
        status_change("Invalid guess");
        return;
    }
    var colors = check(target, guess);
    fill(row_idx, colors);
    for(let i = 0; i < 5; i++){
        var row = rows[row_idx];
        row.children[i].innerHTML = guess.charAt(i);
    }
    var win = true;
    for(let i = 0; i < 5; i++){
        if(colors[i] !== "green"){
            win = false;
            break;
        }
    }
    if(win){
        status_change("You win!");
        return;
    }
    row_idx++;
    if(row_idx >= document.getElementsByTagName("tr").length){
        status_change("You lose!");
        return;
    }
    status_change("You have "+(6-row_idx)+" chances");
}
function fill(row_num, colors){
    var row = rows[row_num];
    var n = row.children.length;
    for(let i = 0; i < n; i++){
        row.children[i].style.background = colors[i];
    }
}
function check(target, guess){
    var n = target.length;
    var list = ["lightgray","lightgray","lightgray","lightgray","lightgray"];
    var guess_dic = {};
    // check green
    for(let i = 0; i < n; i++){
        if(target.charAt(i) === guess.charAt(i)){
            list[i] = "green";
            let ch = target.charAt(i);
            if(guess_dic[ch] == null){
                guess_dic[ch] = 0;
            }
            guess_dic[ch] = guess_dic[ch]+1;
        }
    }
    //check orange
    for(let i = 0; i < n; i++){
        if(list[i] === "green") continue;
        let ch = guess.charAt(i);
        if(Object.keys(target_dic).includes(ch)){
            if(!Object.keys(guess_dic).includes(ch)){
                guess_dic[ch] = 0;
            }
            if(guess_dic[ch] < target_dic[ch]){
                list[i] = "yellow"
            }
            guess_dic[ch] = guess_dic[ch]+1;
        }
    }
    return list;
}