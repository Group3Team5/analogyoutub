let chat_panel_length = 300

let current_visible = 'empty'
let current_chat = ''

let empty_panel_start_x
let empty_panel_width

let new_chat_panel_start_x
let new_chat_panel_width

let find_panel_start_x
let find_panel_width

let message_panel_start_x
let message_panel_width

let user_panel_start_x = window.innerWidth - 210
let user_panel_width = 200






let empty_panel = document.getElementById('empty-panel-id')

let new_chat_panel = document.getElementById('new-chat-panel-id')
let find_panel = document.getElementById('find-chat-panel-id')

let message_panel = document.getElementById('message-panel-id')
let user_panel = document.getElementById('user-panel-id')



let link_new_chat = document.getElementById('link-find-input-id')
let open_chats_box = document.getElementById('open-chats-box-id')
let chats_box = document.getElementById('chat-panel-chats-id')

let messages_box = document.getElementById('messages-box-id')
let users_box = document.getElementById('users-box-id')
let messages_name = document.getElementById('chat-chats-chatname-id')

let send_box = document.getElementById('send-message-id')

let new_chat_input = document.getElementById('new-chat-id')



function updateOpenChatsBox() {
     open_chats_box.style.width = (find_panel_width-40).toString()
}

function updateEmptyWindow() {
     if (current_visible === 'empty') {
          empty_panel_start_x = chat_panel_length + 10
          empty_panel_width = window.innerWidth - (chat_panel_length + 30)

          empty_panel.style.marginLeft = empty_panel_start_x.toString()+'px'
          empty_panel.style.width = empty_panel_width.toString()+'px'

          empty_panel.style.display = 'block'
     } else {
          empty_panel.style.display = 'none'
     }
}

function updateNewChatWindow() {
     if (current_visible === 'new') {
          new_chat_panel_start_x = chat_panel_length + 10
          new_chat_panel_width = window.innerWidth - (chat_panel_length + 30)

          new_chat_panel.style.marginLeft = new_chat_panel_start_x.toString()+'px'
          new_chat_panel.style.width = new_chat_panel_width.toString()+'px'

          new_chat_input.style.width = (new_chat_panel_width - 250).toString() + 'px'

          new_chat_panel.style.display = 'block'
     } else {
          new_chat_panel.style.display = 'none'
     }
}

function updateFindWindow() {
     if (current_visible === 'find') {
          find_panel_start_x = chat_panel_length + 10
          find_panel_width = window.innerWidth - (chat_panel_length + 30)

          find_panel.style.marginLeft = find_panel_start_x.toString()+'px'
          find_panel.style.width = find_panel_width.toString()+'px'

          updateOpenChatsBox()

          find_panel.style.display = 'block'
     } else {
          find_panel.style.display = 'none'
     }
}



function updateChatWindow() {
     if (current_visible === 'chat') {
          message_panel_start_x = chat_panel_length + 10
          user_panel_start_x = window.innerWidth - (user_panel_width + 120)

          message_panel_width = user_panel_start_x - (chat_panel_length + 20)

          message_panel.style.marginLeft = message_panel_start_x.toString()+'px'
          message_panel.style.width = message_panel_width.toString()+'px'

          send_box.style.width = (message_panel_width - 70).toString()+'px'

          message_panel.style.display = 'block'

          user_panel.style.marginLeft = user_panel_start_x.toString()+'px'
          user_panel.style.width = user_panel_width.toString()+'px'

          fillChatsDisplays()

          user_panel.style.display = 'block'


     } else {
          message_panel.style.display = 'none'
          user_panel.style.display = 'none'
     }
}

async function updateChats() {
     await axios.get('/back_end_api/chat/?filter=user').then((response) =>{
          fillChats(response.data.chats)
     })
}

function updateUI() {
     updateEmptyWindow()
     updateNewChatWindow()
     updateFindWindow()
     updateChatWindow()
     updateChats()
}









console.log(window.innerWidth)

updateUI()

window.addEventListener('resize', () => {
     updateUI()
});



function showCreateNewChat() {
     current_visible = 'new'
     current_chat = ''
     updateUI()
}

async function showFindChat() {
     current_visible = 'find'
     current_chat = ''

     axios.get('/back_end_api/chat/?filter=open')
         .then((response) => {
              fillChatBox(response.data.chats)
         }).catch((error) => {
              console.log(error)
          })

     updateUI()
}

function showChat(slug) {
     current_visible = 'chat'
     current_chat = slug
     updateUI()
}





async function findChat() {
     await axios.get(link_new_chat.value).then((response) =>{
               current_visible = 'chat'
         })
}

async function addChat(str) {
     await axios.get('/back_end_api/chat/'+str+'/link/').then((response) =>{
               current_visible = 'chat'
               current_chat = str
               updateUI()
         }).catch((err) => {
              console.log(err)
     })
}


function fillChatBox(dict) {
     open_chats_box.innerHTML = ''
     for (i in dict){
          console.log(dict[i]["slug"] )
          inner = '<div class="chat-info">' +
              '<div class="chat-info-name">'+dict[i]["name"]+'</div>' +
              '<div class="chat-info-link" onclick="addChat(\'' +
               dict[i]["slug"] +
              '\')">Добавить</div>' +
              '<div class="chat-info-n">'+dict[i]["n_subscribes"]+'</div>' +
              '</div>' +
              '<hr class="sep">'
          open_chats_box.innerHTML +=inner
     }

}

function fillChats(dict) {
     chats_box.innerHTML = ''
     for (i in dict){
          console.log(i)
          inner = '<div class="btn-chat-panel"' +
              'onclick="showChat(\''+dict[i]["slug"] +
                  '\')">'+ dict[i]["name"]+'</div>'
          chats_box.innerHTML +=inner
     }

}

async function fillChatsDisplays() {

     await axios.get('/back_end_api/chat/'+ current_chat+'/').then((ressponse) => {
          messages_name.innerText = ressponse.data.chat.name
          fillMessageBox(ressponse.data.messages)
          filluserBox(ressponse.data.chat.n_subscribes)
     })
}

function fillMessageBox(dict){
     messages_box.innerHTML = ''
     for (i in dict){
          console.log(i)
          inner = '<div class ="message">' +
              '<div class="message-sender">' + dict[i]["sender"] +
              '</div>' +
              '<div class="message-text">' +
              dict[i]["text"]+
              '</div>\n' +
              '</div>'
          messages_box.innerHTML +=inner
     }
}
function filluserBox(l){
     users_box.innerHTML = ''
     for (i in l){
          console.log(i)
          inner = '<div class ="users-chats-username">' +
              l[i]+'</div>'
          users_box.innerHTML +=inner
     }
}

function appendMessage(text, username) {
     inner = '<div class ="message">' +
              '<div class="message-sender">' + username +
              '</div>' +
              '<div class="message-text">' +
              text
              '</div>\n' +
              '</div>'
          messages_box.innerHTML +=inner
}

function send(user) {
     if (send_box.value)
          axios.defaults.xsrfCookieName = 'csrftoken'
          axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
          axios.post('/back_end_api/chat/' + current_chat + '/messages/',
              {'text': send_box.value}).then((response) => {
               appendMessage(send_box.value, user)
               send_box.value = ''
          })
}

async function create_new() {
     axios.defaults.xsrfCookieName = 'csrftoken'
     axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
     await axios.post('/back_end_api/chat/',{'name': new_chat_input.value}).then((response) => {
          new_chat_input.value = ''
          current_visible = 'empty'
          updateUI()
     })
}