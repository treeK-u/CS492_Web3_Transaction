import json
import hexbytes
import uuid
from datetime import datetime, timedelta


from web3 import Web3, HTTPProvider
from flask import Flask, render_template, jsonify, request, url_for, redirect

app = Flask(
    __name__,
    static_url_path='',
    static_folder='static',
    template_folder='templates'
)

# conn = Web3(HTTPProvider('http://127.0.0.1:7545'))
conn = Web3(HTTPProvider('http://54.91.173.221:7545'))
network_id = '1685279260059'

# Load Smart Contract - Market
with open('/home/ubuntu//transaction-truffle/build/contracts/Market.json') as f:
    result = json.loads(f.read())
contract = conn.eth.contract(abi=result['abi'], address=result['networks'][network_id]['address'])

# Load Smart Contract - Market
with open('/home/ubuntu/transaction-truffle/build/contracts/UserHistory.json') as f:
    result = json.loads(f.read())
history_contract = conn.eth.contract(abi=result['abi'], address=result['networks'][network_id]['address'])


@app.before_request
def before_request():
    global conn
    if not conn.is_connected():
        conn = Web3(HTTPProvider('http://127.0.0.1:7545'))
    return


@app.after_request
def handle_credentials(response):
    if not request.cookies.get('w3_sid', None):
        response.set_cookie('w3_sid', str(uuid.uuid4()))
    return response


@app.errorhandler(404)
def error_handler(e):
    return redirect('/')


@app.errorhandler(500)
def page_not_found(e):
    return redirect('/')


# ==========================================================================
# ============= Frontend ====================================================
# ==========================================================================


@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/product_detail')
def product_detail():
    return render_template('product_detail.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/upload_item')
def upload_item():
    return render_template('upload_item.html')


@app.route('/user_login_history')
def user_history():
    return render_template('user_login_history.html')


# ==========================================================================
# ============= Backend ====================================================
# ==========================================================================


@app.route('/get_contract_history')
def get_contract_history():
    result = []
    target_address = request.args.get('address')
    for block_num in range(conn.eth.get_block_number() + 1):
        block = conn.eth.get_block(block_num)
        for transaction in dict(block)["transactions"]:
            _info = dict(conn.eth.get_transaction(transaction.hex()))
            _info['timestamp'] = datetime.utcfromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S')

            _from = _info["from"].lower() if _info["from"] else _info["from"]
            _to = _info["to"].lower() if _info["to"] else _info["to"]

            _address = [_from, _to]
            if target_address.lower() in _address and (contract.address.lower() in _address or history_contract.address.lower() in _address):
                result.append(
                    {k: v.hex() if isinstance(v, hexbytes.main.HexBytes) else v for k, v in _info.items()}
                )
    return jsonify(result)


@app.route('/get_transaction_history')
def get_transaction_history():
    result = []
    target_address = request.args.get('address')
    for block_num in range(conn.eth.get_block_number() + 1):
        block = conn.eth.get_block(block_num)
        for transaction in dict(block)["transactions"]:
            _info = dict(conn.eth.get_transaction(transaction.hex()))
            _info['timestamp'] = datetime.utcfromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S')

            _from = _info["from"].lower() if _info["from"] else _info["from"]
            _to = _info["to"].lower() if _info["to"] else _info["to"]

            if target_address.lower() in [_to, _from] and _from and _to:
                result.append(
                    {k: v.hex() if isinstance(v, hexbytes.main.HexBytes) else v for k, v in _info.items()}
                )
    return jsonify(result)


@app.route('/get_commodity_list')
def get_commodity_list():
    """
    Query string에 target_address가 있으면, 해당 address가 올린 상품만 가져오기
    없으면, 전체 가져오기
    :return:
    """
    target_address = request.args.get('address')
    result = []

    for i in range(contract.functions.commodityCount().call()):
        _raw_result = contract.functions.commodityList(i + 1).call()

        _url = url_for('product_detail', id=_raw_result[0])
        _img = url_for('static', filename=f'img/{_raw_result[5]}')
        _user_profile_url = url_for('profile', address=_raw_result[7])

        _flag = (_raw_result[7].lower() == target_address.lower()) if target_address else True
        if _flag:
            result.append([
                f'<img src="{_img}" style="max-width:100%; max-height:100%" />',  # img
                _raw_result[4],  # category
                _raw_result[0],  # id
                _raw_result[1],  # name
                _raw_result[2],  # price
                _raw_result[3],  # is Sold,
                f'<a href="{_user_profile_url}">{_raw_result[7]}</a>',  # sellerAddress
                f'<a href="{_url}">Link</a>'  # Link
            ])
    return jsonify(result)


@app.route('/get_commodity')
def get_commodity():
    if not request.args.get('id').isdigit():
        return jsonify({})

    _id = int(request.args.get('id'))
    if 1 <= _id <= contract.functions.commodityCount().call():
        _raw_result = contract.functions.commodityList(
            _id
        ).call()

        _url = url_for('product_detail', id=_raw_result[0])
        _img = url_for('static', filename=f'img/{_raw_result[5]}')

        result = {
            'imgPath': _img,
            'category': _raw_result[4],  # category
            'id': _raw_result[0],  # id
            'name': _raw_result[1],  # name
            'price': _raw_result[2],  # price
            'isSold': _raw_result[3],  # is Sold
            'description': _raw_result[6],  # description
            'sellerAddress': _raw_result[7],  # Seller Address
        }
    else:
        result = {}
    return jsonify(result)


@app.route('/create_commodity', methods=['POST'])
def create_commodity():
    form_data = request.form

    address = conn.to_checksum_address(form_data['address'])
    imgFile = request.files['imgFile']
    imgFile.save(f'/home/ubuntu/transaction-flask/static/img/{imgFile.filename}')

    referrer = request.headers.get("Referer")
    referrer = referrer if referrer else '/upload_item'

    tx_hash = contract.functions.createCommodity(
        form_data["item-name"],
        int(form_data["item-price"]),
        form_data["category"],
        imgFile.filename,
        form_data["description"],
        address
    ).transact({
        'from': address
    })
    print(conn.eth.wait_for_transaction_receipt(tx_hash))

    return redirect('/home')


@app.route('/update_history')
def update_history():
    sid = request.args.get('sid')
    address = conn.to_checksum_address(request.args.get('address'))

    current_timestamp = (datetime.utcnow() + timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')
    user_info = history_contract.functions.historyList(sid).call()
    if user_info[0]:
        history_contract.functions.updateHistory(sid, address, current_timestamp).transact({
            'from': address
        })
    else:
        history_contract.functions.createHistory(sid, address, current_timestamp).transact({
            'from': address
        })
    return jsonify({'result': True})


@app.route('/get_user_history')
def get_user_history():
    result = []
    for i in range(1, history_contract.functions.userCount().call() + 1):
        _sid = history_contract.functions.idSidTable(i).call()
        result.append(
            history_contract.functions.historyList(_sid).call()
        )
    return jsonify(result)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
