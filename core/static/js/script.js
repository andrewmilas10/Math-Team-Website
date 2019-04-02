var menu = false;

function showMenu(){
  if(menu==false){
    document.getElementById('navBar').style.display = "block";
  }else{
    document.getElementById('navBar').style.display = "none";
  }
  menu = !menu;
}
