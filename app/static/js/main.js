/*--Event Listeners--*/
const userUpdateForm = document.querySelector("userUpdateForm");
if(userUpdateForm) {
    userUpdateForm.addEventListener("submit", function(e) {
        submitUserForm(e, this);
    });
}

