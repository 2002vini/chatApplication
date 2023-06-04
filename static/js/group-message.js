// const chatRoomName = document.getElementById('chatroom_slug').innerHTML;
const chatroom_id = JSON.parse(document.getElementById('json-chatroom').textContent)
const username = JSON.parse(document.getElementById('json-username').textContent)

// Create a new WebSocket
const chatSocket = new WebSocket('ws://'+ window.location.host +'/ws/direct/' + chatroom_id+"/");     // NOTE: window.location.host returns the host address dynamically "127.0.0.1:8080"


chatSocket.onmessage = function(e){
    data = JSON.parse(e.data)
    let message = data.message
    let other_username = data.username
    console.log(data)



    if (data.type == 'chat'){
        let html = `<div class="message">
                        <div>
                            <b>${other_username}</b> <br>
                        </div>
                        <div>
                            ${message} <br>
                        </div>
                        <small class="text-muted">
                            just now<br>
                        </small>
                        <br>
                    </div>`

        document.getElementById('chats').insertAdjacentHTML('beforeend', html)
    }

    scroll();       // whenever we get a new message we will scroll to top
}

document.getElementById('send-button').onclick = function(e){
    e.preventDefault();     // prevent form submission cause we want to send this message via our web socket
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value;
    messageInput.value = ""

    chatSocket.send(JSON.stringify({
        'message': message,
        'username': username,
        'room': chatroom_id
    }))
}


function scroll(){
    const mcontainer = document.getElementById('chat-container');
    mcontainer.scrollTop = mcontainer.scrollHeight;
}

scroll()




//javascript object->json object
//JSON.stringify()
//json object->javascript object
//JSON.parse()

//python object->json obj
//json.dumps()
//json obj->python obj
//json.loads()
