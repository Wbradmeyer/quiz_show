const displayPopup = (itemId) => {
    document.getElementById(`delete_confirm_${itemId}`).style.display = 'block'
}

const hidePopup = (itemId) => {
    document.getElementById(`delete_confirm_${itemId}`).style.display = 'none'
}