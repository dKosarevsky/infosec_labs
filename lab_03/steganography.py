import streamlit as st
import requests

from PIL import Image, ImageDraw, UnidentifiedImageError
from urllib.parse import urlparse
from random import randint
from io import BytesIO

FILE_TYPES = ["png", "bmp"]
URL = "https://allaircraft.ru/uploads/posts/2012-06/1339848718_pak-fa1.png"


def get_image_download_link(img):
    img.save("img.png")
    with open("img.png", "rb") as file:
        return st.download_button(
            label="Сохранить изображение",
            data=file,
            file_name="info_security_lab.png",
            mime="image/png"
        )


def uploader(file):
    show_file = st.empty()
    if not file:
        show_file.info("valid file extension: " + ", ".join(FILE_TYPES))
        return False
    return file


def not_valid_url_err():
    return st.error("Не похоже на ссылку с изображением, повторите ввод.")


def validate_url(url):
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return url
        elif not url:
            not_valid_url_err()
            return False
        else:
            not_valid_url_err()
            return False
    except AttributeError:
        not_valid_url_err()
        return False


def get_image(user_img, user_url):
    img = None
    if user_img is not False:
        img = Image.open(user_img)
    else:
        response = requests.get(user_url)
        try:
            img = Image.open(BytesIO(response.content))
        except UnidentifiedImageError:
            st.write("Что-то пошло не так... Попробуйте другую ссылку или загрузите изображение со своего устройства.")
            st.stop()
    st.image(img)
    get_image_download_link(img)
    return img


def encrypt_cyrillic(letter):
    return letter.encode('cp1251')


def encrypt(img, message):
    keys = []
    draw_object = ImageDraw.Draw(img)
    width = img.size[0]
    height = img.size[1]
    pixels = img.load()

    # for elem in ([ord(encrypt_cyrillic(elem)) for elem in message]):
    for elem in ([ord(elem) for elem in message]):
        key = (randint(1, width - 10), randint(1, height - 10))
        g, b = pixels[key][1:3]
        draw_object.point(key, (elem, g, b))
        # keys += str(key) + "\n"
        keys.append(key)

    st.write("Ключи:")
    st.code(keys)
    st.write("Изображение с зашифрованным текстом:")
    st.image(img)
    get_image_download_link(img)
    return keys, img


def decrypt(img, keys):
    a = []
    pixels = img.load()
    for key in keys:
        a.append(pixels[key][0])
    res = ''.join([chr(elem) for elem in a])
    st.write(res)


def main():
    st.markdown("### Лабораторная работа №3")
    st.markdown("**Тема:** Реализовать стеганографию")
    st.markdown("""
        **Стеганография** 
    — это способ передачи или хранения информации с учётом сохранения в тайне самого факта такой передачи (хранения).
    """)
    st.markdown("---")

    user_img = uploader(st.file_uploader("Загрузить изображение:", type=FILE_TYPES))
    user_url = validate_url(st.text_input(f"Вставьте ссылку на изображение {FILE_TYPES}: ", URL))

    img = get_image(user_img, user_url)

    message = st.text_area(
        "Введите сообщение для шифрования:",
        value="Hello, steganography!"
        # value="Самые ужасные строения — это те, бюджет которых был слишком велик для поставленных целей."
    )

    st.button("Шифровать")
    keys, encrypted_image = encrypt(img, message)

    st.button("Дешифровать")
    decrypt(encrypted_image, keys)


if __name__ == "__main__":
    main()
