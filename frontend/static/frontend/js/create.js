let video
var video_name_field = document.getElementById("video_name_field")


function getVideo(input) {
    video = input.files[0]
}
var csrftoken = getCookie('csrftoken')
function createVideo() {
    if (video.name) {
        $.ajax({
            url: '/back_end_api/video/',
            method: 'post',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: {'name': video_name_field.value},
            success: function (data) {
                if (data.response) {
                    video_name_field.value = ''
                    video_name_field.placeholder = 'Отправка'
                    var formData = new FormData()
                    formData.append('X-CSRFToken', csrftoken)
                    formData.append('slug', data.slug)
                    formData.append('video', video)

                    $.ajax({
                    url: '/video/load_video/',
                    type: 'post',
                    dataType: 'json',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {formData},
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        window.location.href = '/'
                    }})

                } else {
                    video_name_field.value = ''
                    video_name_field.placeholder = data.error

                }


            }
        })
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}