class PlayFairCipher:
    def __init__(self):
        pass

    def create_playfair_matrix(self, key: str):
        # Normalize key: uppercase, replace J with I, keep only letters in alphabet
        key = "".join([c for c in key.upper() if c.isalpha()])
        key = key.replace("J", "I")
        if not key:
            raise ValueError("Key must contain at least one alphabetic character.")

        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        seen = set()
        matrix = []
        
        for char in key:
            if char not in seen and char in alphabet:
                seen.add(char)
                matrix.append(char)
                
        for char in alphabet:
            if char not in seen:
                seen.add(char)
                matrix.append(char)
                
        playfair_matrix = [matrix[i:i+5] for i in range(0, len(matrix), 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col
        # Fallback if a character is missing, though shouldn't happen for valid Playfair inputs
        return 0, 0

    def playfair_encrypt(self, plain_text: str, matrix):
        # Normalize plain text: keep only letters, upper case, J -> I
        plain_text = "".join([c for c in plain_text.upper() if c.isalpha()])
        plain_text = plain_text.replace("J", "I")
        if not plain_text:
            raise ValueError("Plain text must contain at least one alphabetic character.")

        # Preprocess text to separate duplicate letters in a pair and ensure even length
        processed_text = []
        i = 0
        while i < len(plain_text):
            char1 = plain_text[i]
            processed_text.append(char1)
            if i + 1 < len(plain_text):
                char2 = plain_text[i+1]
                if char1 == char2:
                    # Insert filler letter 'X' (or 'Q' if the letter itself is 'X')
                    filler = 'Q' if char1 == 'X' else 'X'
                    processed_text.append(filler)
                    i += 1
                else:
                    processed_text.append(char2)
                    i += 2
            else:
                # Odd length, append filler letter 'X' (or 'Q' if last char is 'X')
                filler = 'Q' if char1 == 'X' else 'X'
                processed_text.append(filler)
                i += 1
                
        plain_text = "".join(processed_text)
        encrypted_text = ""

        for i in range(0, len(plain_text), 2):
            pair = plain_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])
            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]
        return encrypted_text

    def playfair_decrypt(self, cipher_text: str, matrix):
        cipher_text = "".join([c for c in cipher_text.upper() if c.isalpha()])
        cipher_text = cipher_text.replace("J", "I")
        if not cipher_text:
            raise ValueError("Cipher text must contain at least one alphabetic character.")

        decrypted_text = []
        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            if len(pair) < 2:
                decrypted_text.append(pair)
                continue
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                decrypted_text.append(matrix[row1][(col1 - 1) % 5])
                decrypted_text.append(matrix[row2][(col2 - 1) % 5])
            elif col1 == col2:
                decrypted_text.append(matrix[(row1 - 1) % 5][col1])
                decrypted_text.append(matrix[(row2 - 1) % 5][col2])
            else:
                decrypted_text.append(matrix[row1][col2])
                decrypted_text.append(matrix[row2][col1])
                
        decrypted_str = "".join(decrypted_text)
        
        # Postprocess: remove inserted filler characters
        cleaned_text = []
        i = 0
        while i < len(decrypted_str):
            cleaned_text.append(decrypted_str[i])
            if i + 2 < len(decrypted_str):
                char1 = decrypted_str[i]
                filler = decrypted_str[i+1]
                char2 = decrypted_str[i+2]
                if char1 == char2:
                    if (char1 != 'X' and filler == 'X') or (char1 == 'X' and filler == 'Q'):
                        cleaned_text.append(char2)
                        i += 3
                        continue
            i += 1
            
        # Strip trailing filler if it was added for padding
        if len(cleaned_text) > 1:
            last_char = cleaned_text[-1]
            second_last = cleaned_text[-2]
            if (last_char == 'X' and second_last != 'X') or (last_char == 'Q' and second_last == 'X'):
                cleaned_text.pop()
                
        return "".join(cleaned_text)
