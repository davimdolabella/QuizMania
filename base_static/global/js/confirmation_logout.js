document.addEventListener("DOMContentLoaded", function () {
    const logoutForm = document.getElementById("logout-form");
    const logoutButton = logoutForm.querySelector("button");
    const confirmationBox = document.querySelector(".confirmation-logout");
    const confirmLogout = confirmationBox.querySelector(".logout");
    const cancelLogout = confirmationBox.querySelector(".cancel");

    // Impedir o envio direto do formulário e mostrar a caixa de confirmação
    logoutButton.addEventListener("click", function (e) {
        e.preventDefault();
        confirmationBox.classList.remove("none"); // Mostra a confirmação
    });

    // Se confirmar, submete o formulário
    confirmLogout.addEventListener("click", function () {
        logoutForm.submit();
    });

    // Se cancelar, esconde a confirmação
    cancelLogout.addEventListener("click", function () {
        confirmationBox.classList.add("none");
    });
});
