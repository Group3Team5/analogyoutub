usernameField = document.getElementById(id="nameField")
passwordField = document.getElementById(id="passwordField")
errorMessageField = document.getElementById(id="errorMessage")


async function doRequest() {
    request_data = {
        'username' : usernameField.value,
        'password' : passwordField.value
    }

    await axios
        .post('/back_end_api/pasport/user/login/', request_data)
        .then(function (response) {
            window.location.href = '/video/'
        }).catch(function (error) {
            console.log(error)
            errorMessageField.innerText = 'Неверный логин или пароль'
        })
}







