async function loadUser() {

    const tg = window.Telegram.WebApp;

    tg.ready();

    const user = tg.initDataUnsafe.user;

    if (!user) {
        console.log("Open inside Telegram");
        return;
    }

    const telegramId = user.id;

    const response = await fetch(
        `https://click2earn-f6ul.onrender.com/api/user/${telegramId}`
    );

    const data = await response.json();

    document.querySelector(".balance h1").innerText =
        data.balance + " " + data.currency;

}

loadUser();