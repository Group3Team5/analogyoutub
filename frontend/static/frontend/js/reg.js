usernameField = document.getElementById(id="nameField")
passwordField = document.getElementById(id="passwordField")
emailField = document.getElementById(id="emailField")
password2Field = document.getElementById(id="password2Field")
errorMessageField = document.getElementById(id="errorMessage")


async function doRequest() {
    request_data = {
        'username' : usernameField.value,
        'password' : passwordField.value,
        'email' : emailField.value,
        'password2' : password2Field.value
    }

    await axios
        .post('/back_end_api/pasport/user/reg/', request_data)
        .then(function (response) {
            window.location.href = '/video/'
        }).catch(function (error) {
            console.log(error)
            errorMessageField.innerText = 'Неверный данные'
        })
}







