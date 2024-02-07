const displayPopup = (e) => {
    e.preventDefault()
    document.getElementById('delete_confirm').style.display = 'block'
}

const hidePopup = (e) => {
    e.preventDefault()
    document.getElementById('delete_confirm').style.display = 'none'
}