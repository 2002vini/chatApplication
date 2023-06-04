// const chatRoomName = document.getElementById('chatroom_slug').innerHTML;
const chatroom_id = JSON.parse(document.getElementById('json-chatroom').textContent)
const logged_in_user = JSON.parse(document.getElementById('json-username').textContent)

// Create a new WebSocket
const chatSocket = new WebSocket('ws://'+ window.location.host +'/ws/direct/' + chatroom_id+"/");     // NOTE: window.location.host returns the host address dynamically "127.0.0.1:8080"


chatSocket.onmessage = function(e){
    data = JSON.parse(e.data)
    let message = data.message

    let html = `<tr>
                    <td>
                        <p class="bg-success float-right chat_message p-2 mt-2 mr-5 shadow-sm text-white rounded ">
                            ${message}
                            <small class="ml-2" style="font-size: 12px; color:#8FBEA6;">just now</small>
                        </p>
                    </td>
                </tr> `

    document.getElementById('displayed_messages').insertAdjacentHTML('beforeend', html)

    scroll();       // whenever we get a new message we will scroll to top
}

document.getElementById('send-button').onclick = function(e){
    e.preventDefault();     // prevent form submission cause we want to send this message via our web socket
    const messageInput = document.getElementById('message-input');
    const chat_message = messageInput.value;
    messageInput.value = ""

    console.log(chat_message)

    chatSocket.send(JSON.stringify({
        'chat_message_content': chat_message,
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
