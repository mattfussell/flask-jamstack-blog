// selections
const curYrTag = document.querySelector('.currentYear')

// functions
const setCurrentYear = _ => curYrTag.innerText = new Date().getFullYear()

// call functions
setCurrentYear()