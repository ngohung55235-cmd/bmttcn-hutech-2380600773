from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher

app = Flask(__name__)

# CAESAR CIPHER ALGORITHM
caesar_cipher = CaesarCipher()

@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    data = request.json
    plain_text = data['plain_text']
    try:
        key = int(data['key'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Key must be an integer'}), 400
    
    if not (1 <= key <= 25):
        return jsonify({'error': 'Key must be between 1 and 25'}), 400
        
    encrypted_text = caesar_cipher.encrypt_text(plain_text, key)
    return jsonify({'encrypted_message': encrypted_text})

@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    data = request.json
    cipher_text = data['cipher_text']
    try:
        key = int(data['key'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Key must be an integer'}), 400

    if not (1 <= key <= 25):
        return jsonify({'error': 'Key must be between 1 and 25'}), 400
        
    decrypted_text = caesar_cipher.decrypt_text(cipher_text, key)
    return jsonify({'decrypted_message': decrypted_text})

# VIGENERE CIPHER ALGORITHM
vigenere_cipher = VigenereCipher()

@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    data = request.json
    plain_text = data.get('plain_text', '')
    key = data.get('key', '')
    if not key or not key.isalpha():
        return jsonify({'error': 'Key must contain only alphabetic characters and cannot be empty'}), 400
    try:
        encrypted_text = vigenere_cipher.vigenere_encrypt(plain_text, key)
        return jsonify({'encrypted_text': encrypted_text})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    data = request.json
    cipher_text = data.get('cipher_text', '')
    key = data.get('key', '')
    if not key or not key.isalpha():
        return jsonify({'error': 'Key must contain only alphabetic characters and cannot be empty'}), 400
    try:
        decrypted_text = vigenere_cipher.vigenere_decrypt(cipher_text, key)
        return jsonify({'decrypted_text': decrypted_text})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

# RAILFENCE CIPHER ALGORITHM
railfence_cipher = RailFenceCipher()

@app.route('/api/railfence/encrypt', methods=['POST'])
def railfence_encrypt():
    data = request.json
    plain_text = data.get('plain_text', '')
    try:
        key = int(data['key'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Key must be an integer'}), 400

    if len(plain_text) < 2:
        return jsonify({'error': 'Text length must be at least 2 to use Rail Fence cipher'}), 400
    if key < 2:
        return jsonify({'error': 'Key must be at least 2'}), 400
    if key >= len(plain_text):
        return jsonify({'error': 'Key must be less than the text length'}), 400

    try:
        encrypted_text = railfence_cipher.rail_fence_encrypt(plain_text, key)
        return jsonify({'encrypted_text': encrypted_text})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/railfence/decrypt', methods=['POST'])
def railfence_decrypt():
    data = request.json
    cipher_text = data.get('cipher_text', '')
    try:
        key = int(data['key'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Key must be an integer'}), 400

    if len(cipher_text) < 2:
        return jsonify({'error': 'Text length must be at least 2 to use Rail Fence cipher'}), 400
    if key < 2:
        return jsonify({'error': 'Key must be at least 2'}), 400
    if key >= len(cipher_text):
        return jsonify({'error': 'Key must be less than the text length'}), 400

    try:
        decrypted_text = railfence_cipher.rail_fence_decrypt(cipher_text, key)
        return jsonify({'decrypted_text': decrypted_text})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

# PLAYFAIR CIPHER ALGORITHM
playfair_cipher = PlayFairCipher()

@app.route('/api/playfair/creatematrix', methods=['POST'])
def playfair_creatematrix():
    data = request.json
    key = data.get('key', '')
    if not any(c.isalpha() for c in key):
        return jsonify({'error': 'Key must contain at least one alphabetic character'}), 400
    try:
        playfair_matrix = playfair_cipher.create_playfair_matrix(key)
        return jsonify({"playfair_matrix": playfair_matrix})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    data = request.json
    plain_text = data.get('plain_text', '')
    key = data.get('key', '')
    if not any(c.isalpha() for c in key):
        return jsonify({'error': 'Key must contain at least one alphabetic character'}), 400
    if not any(c.isalpha() for c in plain_text):
        return jsonify({'error': 'Plain text must contain at least one alphabetic character'}), 400
    try:
        playfair_matrix = playfair_cipher.create_playfair_matrix(key)
        encrypted_text = playfair_cipher.playfair_encrypt(plain_text, playfair_matrix)
        return jsonify({'encrypted_text': encrypted_text})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    data = request.json
    cipher_text = data.get('cipher_text', '')
    key = data.get('key', '')
    if not any(c.isalpha() for c in key):
        return jsonify({'error': 'Key must contain at least one alphabetic character'}), 400
    if not any(c.isalpha() for c in cipher_text):
        return jsonify({'error': 'Cipher text must contain at least one alphabetic character'}), 400
    try:
        playfair_matrix = playfair_cipher.create_playfair_matrix(key)
        decrypted_text = playfair_cipher.playfair_decrypt(cipher_text, playfair_matrix)
        return jsonify({'decrypted_text': decrypted_text})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

# main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
