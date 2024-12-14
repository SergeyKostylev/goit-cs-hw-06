console.log('Hello world!')

const ws = new WebSocket('ws://localhost:5099')

formChat.addEventListener('submit', (e) => {
    e.preventDefault()
    // ws.send(usermessage.value)
    message = {
        name: username.value,
        message: usermessage.value,
    }
    ws.send(JSON.stringify(message))
    usernamediv.style.display = 'none'
    usermessage.value = null
})

ws.onopen = (e) => {
    console.log('Hello WebSocket!')
}

ws.onmessage = (e) => {
    console.log(e.data)
    text = e.data

    const elMsg = document.createElement('div')
    elMsg.textContent = text
    subscribe.appendChild(elMsg)
}

