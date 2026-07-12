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

document.getElementById("watchAdsBtn").onclick = async function () {

    const tg = window.Telegram.WebApp;
    const telegramId = tg.initDataUnsafe.user.id;

    await fetch(
        `https://click2earn-f6ul.onrender.com/api/reward/${telegramId}`,
        {
            method: "POST"
        }
    );

    alert("🎉 +0.001 USDT Reward Added!");

    loadUser();
};