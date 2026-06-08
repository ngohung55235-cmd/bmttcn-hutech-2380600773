from flask import Flask, render_template, request
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher

app = Flask(__name__)

# router routes for home page
@app.route("/")
def home():
    return render_template('index.html')

# ==================== CAESAR CIPHER ====================
@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    try:
        key = int(request.form['inputKeyPlain'])
    except (ValueError, TypeError):
        return "Error: Key must be an integer."
        
    if not (1 <= key <= 25):
        return "Error: Key must be between 1 and 25."
        
    Caesar = CaesarCipher()
    encrypted_text = Caesar.encrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    try:
        key = int(request.form['inputKeyCipher'])
    except (ValueError, TypeError):
        return "Error: Key must be an integer."
        
    if not (1 <= key <= 25):
        return "Error: Key must be between 1 and 25."
        
    Caesar = CaesarCipher()
    decrypted_text = Caesar.decrypt_text(text, key)
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"

# ==================== VIGENERE CIPHER ====================
@app.route("/vigenere")
def vigenere():
    return render_template('vigenere.html')

@app.route("/vigenere_encrypt", methods=['POST'])
def vigenere_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    if not key or not key.isalpha():
        return "Error: Key must contain only alphabetic characters and cannot be empty."

    cipher = VigenereCipher()
    try:
        encrypted_text = cipher.vigenere_encrypt(text, key)
        return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"
    except ValueError as e:
        return f"Error: {str(e)}"

@app.route("/vigenere_decrypt", methods=['POST'])
def vigenere_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    if not key or not key.isalpha():
        return "Error: Key must contain only alphabetic characters and cannot be empty."

    cipher = VigenereCipher()
    try:
        decrypted_text = cipher.vigenere_decrypt(text, key)
        return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"
    except ValueError as e:
        return f"Error: {str(e)}"

# ==================== RAIL FENCE CIPHER ====================
@app.route("/railfence")
def railfence():
    return render_template('railfence.html')

@app.route("/railfence_encrypt", methods=['POST'])
def railfence_encrypt():
    text = request.form['inputPlainText']
    try:
        key = int(request.form['inputKeyPlain'])
    except (ValueError, TypeError):
        return "Error: Key must be an integer."

    if len(text) < 2:
        return "Error: Text length must be at least 2 to use Rail Fence cipher."
    if key < 2:
        return "Error: Key must be at least 2."
    if key >= len(text):
        return "Error: Key must be less than the text length."

    cipher = RailFenceCipher()
    try:
        encrypted_text = cipher.rail_fence_encrypt(text, key)
        return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"
    except ValueError as e:
        return f"Error: {str(e)}"

@app.route("/railfence_decrypt", methods=['POST'])
def railfence_decrypt():
    text = request.form['inputCipherText']
    try:
        key = int(request.form['inputKeyCipher'])
    except (ValueError, TypeError):
        return "Error: Key must be an integer."

    if len(text) < 2:
        return "Error: Text length must be at least 2 to use Rail Fence cipher."
    if key < 2:
        return "Error: Key must be at least 2."
    if key >= len(text):
        return "Error: Key must be less than the text length."

    cipher = RailFenceCipher()
    try:
        decrypted_text = cipher.rail_fence_decrypt(text, key)
        return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"
    except ValueError as e:
        return f"Error: {str(e)}"

# ==================== PLAYFAIR CIPHER ====================
@app.route("/playfair")
def playfair():
    return render_template('playfair.html')

@app.route("/playfair_encrypt", methods=['POST'])
def playfair_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    if not any(c.isalpha() for c in key):
        return "Error: Key must contain at least one alphabetic character."
    if not any(c.isalpha() for c in text):
        return "Error: Plain text must contain at least one alphabetic character."
        
    cipher = PlayFairCipher()
    try:
        matrix = cipher.create_playfair_matrix(key)
        encrypted_text = cipher.playfair_encrypt(text, matrix)
        return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"
    except ValueError as e:
        return f"Error: {str(e)}"

@app.route("/playfair_decrypt", methods=['POST'])
def playfair_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    if not any(c.isalpha() for c in key):
        return "Error: Key must contain at least one alphabetic character."
    if not any(c.isalpha() for c in text):
        return "Error: Cipher text must contain at least one alphabetic character."

    cipher = PlayFairCipher()
    try:
        matrix = cipher.create_playfair_matrix(key)
        decrypted_text = cipher.playfair_decrypt(text, matrix)
        return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"
    except ValueError as e:
        return f"Error: {str(e)}"

# main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)