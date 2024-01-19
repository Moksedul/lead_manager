const pushForm = document.getElementById('notification');
const errorMsg = document.querySelector('.error');




pushForm.addEventListener('submit', async function (e) {
    e.preventDefault();
    const input = this[0];
    const textarea = this[1];
    const button = this[2];
    errorMsg.innerText = '';
    var user = document.getElementById('user').value;
    var body = document.getElementById('body').value;

    if (user && body) {
        button.innerText = 'Sending...';
        button.disabled = true;

        const res = await fetch('/send_push', {
            method: 'POST',
            body: JSON.stringify({user, body}),
            headers: {
                'content-type': 'application/json'
            }
        });
        if (res.status === 200) {
            button.innerText = 'Send another 😃!';
            button.disabled = false;
            input.value = '';
            textarea.value = '';
        } else {
            errorMsg.innerText = res.message;
            button.innerText = 'Something broke 😢..  Try again?';
            button.disabled = false;
        }
    }
    else {
        let error;
        if (!user & !body){
            error = 'You forgot to fill-up the form'
        }
        else if (!body){
            error = "What is the work of nothing!"
        }
        else if (!user){
            error = "Message without receiver can't be sent"
        }
        errorMsg.innerText = error;
    }
});