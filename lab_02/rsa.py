import streamlit as st
import secrets
import sympy


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
        st.write("Модуль (n) = ", n)
        phi_n = (p - 1) * (q - 1)
        st.write("Функция Эйлера от числа n = ", phi_n)

        e = self.fermat_numbers(phi_n)
        st.write("Открытая экспонента е = ", e)

        d = self.modular_inverse(e, phi_n)
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


def main():
    st.markdown("### Лабораторная работа №2")
    st.markdown("**Тема:** Реализация алгоритма шифрования RSA")
    st.markdown("**Цель работы:** Получение навыков построения алгоритма шифрования RSA.")
    st.markdown("---")

    rsa = RSA()

    type_pq = st.radio(
        "Выберите тип получения p и q:", (
            "1. Генерация",
            "2. Ручной ввод",
        )
    )

    p, q = 0, 0
    if type_pq[:1] == "1":
        key_size = st.selectbox("Выберите размер ключа (бит):", [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096], index=7)

        p = rsa.generate_random_prime(key_size)
        q = rsa.generate_random_prime(key_size)
        st.button("Генерировать случайные p и q")

    elif type_pq[:1] == "2":
        c1, c2 = st.columns(2)
        p = c1.number_input("Введите число p:", value=2229283031, step=1)
        q = c2.number_input("Введите число q:", value=3851864347, step=1)

    st.write("p = ", p)
    st.write("q = ", q)

    public_key, private_key = rsa.generate_keys(p, q)

    st.write("Публичный ключ (пара): ", public_key)
    st.write("Приватный ключ (пара): ", private_key)
    st.markdown("---")

    message = st.text_area(
        "Введите сообщение для шифрования:",
        value="Если проект не укладывается в сроки, то добавление рабочей силы задержит его еще больше."
    )
    st.button("Шифровать")

    encrypted = rsa.encrypt(message, public_key)
    show_encrypted = st.checkbox("Показать результат шифрования")
    if show_encrypted:
        st.write(encrypted)

    st.markdown("---")
    st.button("Дешифровать")
    decrypted = rsa.decrypt(encrypted, private_key)
    show_decrypted = st.checkbox("Показать результат дешифровки", True)
    if show_decrypted:
        st.write(decrypted)

    st.markdown("---")


if __name__ == "__main__":
    main()
