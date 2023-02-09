async function sub(any) {
    await axios.get('/back_end_api/video/subscribe/?creator='+any).then((response) => {
        if (document.getElementById(any).innerText === 'Подписаться')
            document.getElementById(any).innerText = 'Отписаться'
        else
            document.getElementById(any).innerText = 'Подписаться'
    })
}

function red(any) {
    window.location.href = '/video/user_video/'+ any +'/'
}