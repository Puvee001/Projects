// Displays the value selected
function display(num){
    document.getElementById("output").value += num
}

//Evaluates the digit and returns the result 
function solve() { 
    let val = document.getElementById("output").value 
    let ans = math.evaluate(val) 
    document.getElementById("output").value = ans 
} 

//Clears the display
function clr() { 
    document.getElementById("output").value = "" 
} 