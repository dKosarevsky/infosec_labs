import streamlit as st
import secrets
import sympy
import time


class RSA:

    def __init__(self):
        pass

    @staticmethod
    def generate_random_prime(length):
        while True:
            num = secrets.randbits(length)
            if num.bit_length() == length:
                if sympy.isprime(num):
                    return num

    @staticmethod
    def euclidean(a, b):
        while b:
            a, b = b, a % b
        return a

    def fermat_numbers(self, n):
        for i in range(5):
            num = 2 ** 2 ** i + 1
            if self.euclidean(num, n) == 1:
                return num
        return -1

    def extended_euclidean(self, a, b):
        if b == 0:
            return a, 1, 0
        else:
            d, x, y = self.extended_euclidean(b, a % b)
            x, y = y, x - (a // b) * y
            return d, x, y

    def modular_inverse(self, a, n):
        _, x, _ = self.extended_euclidean(a, n)
        return x % n

    def generate_keys(self, p, q):
        if sympy.isprime(p) is False or sympy.isprime(q) is False:
            st.error('Число должно быть простым. Повторите ввод или сгенерируйте числа.')
            st.stop()
        elif p == q:
            st.error('Числа p и q не могут быть равны. Повторите ввод или сгенерируйте числа.')
            st.stop()
        n = p * q
        phi_n = (p - 1) * (q - 1)

        e = self.fermat_numbers(phi_n)

        d = self.modular_inverse(e, phi_n)

        show_gen_data = st.checkbox("Показать значения n, φ(n), e и d")
        if show_gen_data:
            st.write("Модуль (n) = ", n)
            st.write("Функция Эйлера от числа n = ", phi_n)
            st.write("Открытая экспонента е = ", e)
            st.write("Секретная экспонента d = ", d)

        return (e, n), (d, n)

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


def gen_pq(rsa):
    key_size = st.selectbox("Выберите размер ключа (бит):", [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096], index=7)

    start = time.time()
    p = rsa.generate_random_prime(key_size)
    q = rsa.generate_random_prime(key_size)
    end = time.time()

    st.form_submit_button("Генерировать случайные p и q")
    st.write(f"Сгенерировано за {round(end - start, 6)} секунд")
    return p, q


def main():
    st.markdown("### Лабораторная работа №2")
    st.markdown("**Тема:** Реализация алгоритма шифрования RSA")
    st.markdown("**Цель работы:** Получение навыков построения алгоритма шифрования RSA.")
    st.markdown("---")

    with st.form("Gen keys"):
        rsa = RSA()

        p, q = gen_pq(rsa)

        show_pq = st.checkbox("Показать сгенерированные p и q")
        if show_pq:
            st.write("p = ", p)
            st.write("q = ", q)

        public_key, private_key = rsa.generate_keys(p, q)

        st.write("Публичный ключ (пара): ", public_key)
        st.write("Приватный ключ (пара): ", private_key)

    with st.form("Encrypt"):
        message = st.text_area(
            "Введите сообщение для шифрования:",
            value="Если проект не укладывается в сроки, то добавление рабочей силы задержит его еще больше."
        )
        st.form_submit_button("Шифровать")

        encrypted = rsa.encrypt(message, public_key)
        show_encrypted = st.checkbox("Показать результат шифрования")
        if show_encrypted:
            st.write(encrypted)

    with st.form("Decrypt"):
        st.form_submit_button("Дешифровать")
        decrypted = rsa.decrypt(encrypted, private_key)
        show_decrypted = st.checkbox("Показать результат дешифровки", True)
        if show_decrypted:
            st.write(decrypted)


if __name__ == "__main__":
    main()
