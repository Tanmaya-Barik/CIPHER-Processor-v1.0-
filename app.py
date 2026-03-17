from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# --- Core Cipher Logic ---
def is_valid_key(key):
    """Validates that the key is exactly 26 unique alphabetic characters."""
    key = key.upper()
    return len(key) == 26 and key.isalpha() and len(set(key)) == 26

def process_encryption(plaintext, key):
    key = key.upper()
    ciphertext = ""
    for char in plaintext.upper():
        if char.isalpha():
            index = ord(char) - ord('A')
            ciphertext += key[index]
        else:
            ciphertext += char
    return ciphertext

def process_decryption(ciphertext, key):
    key = key.upper()
    inverse_key = {key[i]: chr(i + ord('A')) for i in range(26)}
    plaintext = ""
    for char in ciphertext.upper():
        if char.isalpha():
            plaintext += inverse_key[char]
        else:
            plaintext += char
    return plaintext

# --- Web Routes ---
@app.route('/')
def home():
    # Serves the frontend HTML page
    return render_template('index.html')

@app.route('/api/cipher', methods=['POST'])
def cipher_api():
    # Receives data from the frontend
    data = request.get_json()
    action = data.get('action') # 'encrypt' or 'decrypt'
    text = data.get('text', '')
    key = data.get('key', '')

    # Validate the key
    if not is_valid_key(key):
        return jsonify({"error": "Key must contain exactly 26 unique letters (A-Z)."}), 400

    # Perform the chosen action
    if action == 'encrypt':
        result = process_encryption(text, key)
    elif action == 'decrypt':
        result = process_decryption(text, key)
    else:
        return jsonify({"error": "Invalid action."}), 400

    # Send the result back to the frontend
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)