const displayPopup = (questionId) => {
    document.getElementById(`delete_confirm_${questionId}`).style.display = 'block'
}

const hidePopup = (questionId) => {
    document.getElementById(`delete_confirm_${questionId}`).style.display = 'none'
}