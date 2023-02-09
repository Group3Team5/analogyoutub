
async function logout() {
    const response = await axios.get('/back_end_api/pasport/user/login/')

    if(response.data.response)
        window.location.replace('/video/')
}

function red(any) {
    window.location.href = '/video/user_video/'+ any +'/'
}