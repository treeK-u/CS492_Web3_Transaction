async function getAccount() {
    // MetaMask가 설치되어 있는지 확인
    if (typeof window.ethereum !== 'undefined') {
        // MetaMask 연결
        const accounts = await window.ethereum.request({method: 'eth_requestAccounts'});
        return accounts[0]; // 첫 번째 계정 주소 반환
    } else {
        throw new Error('MetaMask를 찾을 수 없습니다.');
    }
}

async function sendETH(price, from, to) {
    try {
        let web3 = new Web3();

        const txHash = await window.ethereum.request({
            method: 'eth_sendTransaction',
            params: [
                {

                    from: from,
                    to: to,
                    // toWei 함수 제거됨 : eth -> wei 공식 : eth * 10^18
                    value: web3.utils.toHex(web3.utils.toWei(price.toString(), "ether")),
                },
            ],
        });

        console.log('트랜잭션 해시:', txHash);
        alert("성공!");
    } catch (error) {
        console.error('오류 발생:', error);
        alert("실패!");
    }
}

async function createCommodity() {
    try {
        console.log("tmp");
    } catch (error) {
        console.log(error);
    }
}
