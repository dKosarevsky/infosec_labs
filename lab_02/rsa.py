import streamlit as st
import random as rnd


class RSA:

    def __init__(self, private_key="", public_key="", random=rnd):
        self.private_key = private_key
        self.public_key = public_key
        self.random = random

    @staticmethod
    def is_prime(num):
        if num == 2:
            return True
        if num < 2 or num % 2 == 0:
            return False
        for n in range(3, int(num ** 0.5) + 2, 2):
            if num % n == 0:
                return False
        return True

    def generate_random_prime(self, max_prime_length):
        while 1:
            ran_prime = self.random.randint(0, max_prime_length)
            if self.is_prime(ran_prime):
                return ran_prime

    @staticmethod
    def euclidean(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def extended_euclidean(self, a, b):
        if a == 0:
            return b, 0, 1
        else:
            d, y, x = self.extended_euclidean(b % a, a)
            return d, x - (b // a) * y, y

    def generate_keys(self):
        p = self.generate_random_prime(10000000000)
        q = self.generate_random_prime(10000000000)

        modulus = p * q
        st.write("Модуль (n) = ", modulus)
        f_mod = (p - 1) * (q - 1)
        st.write("Функция Эйлера от числа n = ", f_mod)

        self.public_key = self.random.randint(1, f_mod)
        d = self.euclidean(self.public_key, f_mod)
        while d != 1:
            self.public_key = self.random.randint(1, f_mod)
            d = self.euclidean(self.public_key, f_mod)

        st.write("Публичный ключ: ", self.public_key)

        self.private_key = self.extended_euclidean(self.public_key, f_mod)[1]

        self.private_key = self.private_key % f_mod
        if self.private_key < 0:
            self.private_key += f_mod

        return (self.private_key, modulus), (self.public_key, modulus)

    @staticmethod
    def encrypt(message, public_key):
        key, n = public_key
        ctext = [pow(ord(char), key, n) for char in message]
        return ctext

    @staticmethod
    def decrypt(message, private_key):
        try:
            key, n = private_key
            text = [chr(pow(char, key, n)) for char in message]
            return "".join(text)
        except TypeError as e:
            st.error(e)


def main():
    st.markdown("### Лабораторная работа №2")
    st.markdown("**Тема:** Реализация алгоритма шифрования RSA")
    st.markdown("**Цель работы:** Получение навыков построения алгоритма шифрования RSA.")
    st.markdown("---")

    a = RSA()
    public_key, private_key = a.generate_keys()
    st.write("Публичный ключ (пара): ", public_key)
    st.write("Приватный ключ (пара): ", private_key)
    st.markdown("---")

    message = st.text_area(
        "Введите сообщение для шифрования:",
        value="Если проект не укладывается в сроки, то добавление рабочей силы задержит его еще больше."
    )
    st.button("Шифровать")

    encrypted = RSA.encrypt(message, public_key)
    st.write("Результат шифрования:", encrypted)

    plaintext = RSA.decrypt(encrypted, private_key)
    st.write(f"Результат дешифровки: {plaintext}")

    st.markdown("---")


if __name__ == "__main__":
    main()
