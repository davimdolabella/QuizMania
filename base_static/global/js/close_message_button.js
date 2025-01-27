buttons = document.querySelectorAll('.close-button')
messages = document.querySelectorAll('.message')
buttons.forEach(button => {
    button.addEventListener('click', () => {
        button.parentElement.style.display = 'none'
    })
});