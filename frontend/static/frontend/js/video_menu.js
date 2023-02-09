let visible = false
let menu = document.getElementById("menu-id")

function showMenu() {
    console.log('s')
    visible = !visible

    if (visible) {
        menu.style.marginLeft = '-5px'
    } else {
        menu.style.marginLeft = '-255px'
    }
}