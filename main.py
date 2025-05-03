import cv2
import numpy as np
import matplotlib.pyplot as plt
import random

def encrypt_image(image, block_size=32, seed=14527):
    h, w, _ = image.shape
    new_h = (h // block_size) * block_size
    new_w = (w // block_size) * block_size
    image = image[:new_h, :new_w]

    blocks = []
    for y in range(0, new_h, block_size):
        for x in range(0, new_w, block_size):
            block = image[y:y + block_size, x:x + block_size]
            blocks.append(((y, x), block))

    random.seed(seed)
    indices = list(range(len(blocks)))
    shuffled_indices = indices.copy()
    random.shuffle(shuffled_indices)

    encrypted = np.zeros_like(image)
    for orig_idx, new_idx in zip(indices, shuffled_indices):
        (y, x), _ = blocks[orig_idx]
        _, block = blocks[new_idx]
        encrypted[y:y + block_size, x:x + block_size] = block

    return encrypted, shuffled_indices, block_size, image  # повертаємо також обрізане зображення

def decrypt_image(encrypted_image, block_size, key):
    h, w, _ = encrypted_image.shape
    decrypted = np.zeros_like(encrypted_image)

    blocks = []
    for y in range(0, h, block_size):
        for x in range(0, w, block_size):
            blocks.append((y, x))

    for idx, shuffled_idx in enumerate(key):
        y, x = blocks[idx]
        sy, sx = blocks[shuffled_idx]
        decrypted[sy:sy + block_size, sx:sx + block_size] = encrypted_image[y:y + block_size, x:x + block_size]

    return decrypted

# === Головна частина ===
image = cv2.imread("images/frame.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

encrypted_image, key, block_size, cropped_image = encrypt_image(image)
decrypted_image = decrypt_image(encrypted_image, block_size, key)

# === Виведення всіх трьох зображень ===
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.imshow(cropped_image)
plt.title("Original Image")
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(encrypted_image)
plt.title("Encrypted Image")
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(decrypted_image)
plt.title("Decrypted Image")
plt.axis('off')

plt.tight_layout()
plt.show()
