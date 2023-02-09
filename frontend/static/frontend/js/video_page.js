let video_container = document.getElementById('video-container-id')
let comments_container = document.getElementById('comments-container-id')
let sub_container = document.getElementById('sub-container-id')

let comments_box = document.getElementById('comments-box-id')

let send_box = document.getElementById('send-message-id')

let messages_box = document.getElementById('comments-box-id')


function updateUI() {
    comments_container.style.width = '350px'
    comments_container.style.height = (window.innerHeight - 80).toString()+'px'
    comments_container.style.marginTop = '48px'
    comments_container.style.marginLeft = (window.innerWidth - 385).toString()+'px'

    sub_container.style.width = (window.innerWidth - 410).toString()+'px'
    sub_container.style.height = '40px'
    sub_container.style.marginTop = (window.innerHeight - 75).toString()+'px'
    sub_container.style.marginLeft = '0px'

    video_container.style.width = (window.innerWidth - 410).toString()+'px'
    video_container.style.height = (window.innerHeight - 160).toString()+'px'
    video_container.style.marginTop = '50px'
    video_container.style.marginLeft = '0px'

    comments_box.style.height = (window.innerHeight - 280).toString()+'px'

}


async function like(str) {
    await axios.get('/back_end_api/video/'+str+'/like/').then((response) => {
        document.getElementById('dislike-id').innerHTML = 'Не нравится: '+response.data.dislikes
        document.getElementById('like-id').innerHTML = 'Нравится: '+response.data.likes
        })
}
async function dislike(str) {
    await axios.get('/back_end_api/video/'+str+'/dislike/').then((response) => {
        document.getElementById('dislike-id').innerHTML = 'Не нравится: '+response.data.dislikes
        document.getElementById('like-id').innerHTML = 'Нравится: '+response.data.likes
        })
}
async function sub(any) {
    await axios.get('/back_end_api/video/subscribe/?creator='+any).then((response) => {
        if (document.getElementById('sub-id').innerText === 'Подписаться')
            document.getElementById('sub-id').innerText = 'Отписаться'
        else
            document.getElementById('sub-id').innerText = 'Подписаться'
    })
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

function send(user, video) {
     if (send_box.value)
          axios.defaults.xsrfCookieName = 'csrftoken'
          axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
          axios.post('/back_end_api/video/' + video + '/comments/',
              {'text': send_box.value}).then((response) => {
               appendMessage(send_box.value, user)
               send_box.value = ''
          })
}







window.addEventListener('resize', () => {
     updateUI()
});

updateUI()