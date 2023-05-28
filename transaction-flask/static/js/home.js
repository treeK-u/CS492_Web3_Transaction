let accounts;

$(document).ready(function() {
    getAccount().then((address) => {
        accounts = address;
        console.log("==");
        console.log(accounts);
        console.log("--");
    })
});
