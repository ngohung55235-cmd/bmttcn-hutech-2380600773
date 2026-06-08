import sys
from PIL import Image

def decode_image(encoded_image_path):
    img = Image.open(encoded_image_path)
    width, height = img.size
    binary_message = ""
    for row in range(height):
        for col in range(width):
            pixel = img.getpixel((col, row))
            
            for color_channel in range(3):
                binary_message += format(pixel[color_channel], '08b')[-1]
                
    message = ""
    found_delimiter = False
    for i in range(0, len(binary_message), 8):
        if i + 8 > len(binary_message):
            break
        char = chr(int(binary_message[i:i+8], 2))
        if char == '\u00fe': # Kết thúc thông điệp khi gặp dấu '\u00fe'
            found_delimiter = True
            break
        message += char
        if len(message) > 256: # Giới hạn độ dài tin nhắn ẩn
            break
            
    if not found_delimiter:
        return "No hidden message found."
        
    return message

def main():
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <encoded_image_path>")
        return
        
    encoded_image_path = sys.argv[1]
    decoded_message = decode_image(encoded_image_path)
    print("Decoded message:", decoded_message)

if __name__ == "__main__":
    main()
