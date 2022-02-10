import streamlit as st
import pandas as pd

from string import ascii_uppercase as alphabet

alpha_len = len(alphabet)


def get_cipher_letter(key, letter):
    if letter in alphabet:
        return alphabet[key]
    else:
        return letter


def caesar_cypher(message, key, type_="en"):
    result = ""

    for letter in message:
        if type_ == "de":
            new_key = (alphabet.index(letter) - key) % alpha_len
        else:
            new_key = (alphabet.index(letter) + key) % alpha_len
        result += get_cipher_letter(new_key, letter)

    return result


def vigenere_cypher(message, key, type_="en"):
    result = ""

    for c in range(len(message)):
        if type_ == "de":
            result += alphabet[(alphabet.index(message[c]) - alphabet.index(key[c])) % alpha_len]
        else:
            result += alphabet[(alphabet.index(message[c]) + alphabet.index(key[c])) % alpha_len]
    return result


def main():
    st.markdown("### Лабораторная работа №1")
    st.markdown("**Тема:** Реализация шифра Цезаря и шифра Виженера")
    st.markdown("**Цель работы:** Получение навыков построения алгоритмов шифрования Цезаря и Виженера.")

    cipher = st.radio(
        "Выберите вид шифра:", (
            "1. Цезарь",
            "2. Виженер",
        )
    )

    if cipher[:1] == "1":
        st.image('lab_01/caesar.png')

        st.markdown("---")
        c1, c2 = st.columns(2)
        mes = c1.text_input("Введите сообщение для шифрования:", value="Apple").upper()
        k = int(c2.number_input("Укажите сдвиг для шифрования:", min_value=1, max_value=26, value=3, step=1))

        encrypted = caesar_cypher(mes, k)
        st.write(f"Результат шифрования: {encrypted}")

        st.markdown("---")
        c11, c22 = st.columns(2)
        mes2 = c11.text_input("Введите сообщение для дешифровки:", value="dssoh").upper()
        k2 = int(c22.number_input("Укажите сдвиг для дешифровки:", min_value=1, max_value=26, value=3, step=1))

        decrypted = caesar_cypher(mes2, k2, type_="de")
        st.write(f"Результат дешифровки: {decrypted}")

        st.markdown("---")

    else:
        st.image('lab_01/vigenere.png', width=600)

        st.markdown("---")
        c3, c4 = st.columns(2)
        mes = c3.text_input("Введите сообщение для шифрования:", value="ATTACKATDAWN").upper()
        k = c4.text_input("Введите ключ для шифрования:", value="Lemon").upper()

        k = (k * len(mes))[:len(mes)]
        data = {"Сообщение": [x for x in mes], "Ключ": [y for y in k]}
        df = pd.DataFrame(data)
        st.write(df.T)

        encrypted = vigenere_cypher(mes, k)
        st.write(f"Результат шифрования: {encrypted}")

        st.markdown("---")
        c33, c44 = st.columns(2)
        mes2 = c33.text_input("Введите сообщение для дешифровки:", value="LXFOPVEFRNHR").upper()
        k2 = c44.text_input("Введите ключ для дешифровки:", value="Lemon").upper()
        k2 = (k2 * len(mes))[:len(mes)]
        st.write(f"Результат дешифровки: {vigenere_cypher(mes2, k2, type_='de')}")

        st.markdown("---")


if __name__ == "__main__":
    main()
