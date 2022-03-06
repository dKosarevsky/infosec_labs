import streamlit as st

from lab_01 import caesar
from lab_02 import rsa
from lab_03 import steganography
from lab_04 import huffman
# from lab_05 import

# st.set_page_config(initial_sidebar_state="collapsed")
st.sidebar.image('logo.png', width=300)


def header():
    author = """
        made by [Kosarevsky Dmitry](https://github.com/dKosarevsky) 
        for [InfoSec](https://github.com/dKosarevsky/iu7/blob/master/8sem/infosec.md) labs
        in [BMSTU](https://bmstu.ru)
    """
    st.header("МГТУ им. Баумана. Кафедра ИУ7")
    st.markdown("**Курс:** Защита информации")
    st.markdown("**Преподаватель:** Кивва К.А.")
    st.markdown("**Студент:** Косаревский Д.П.")
    st.sidebar.markdown(author)


def main():
    header()
    lab = st.sidebar.radio(
        "Выберите Лабораторную работу:", (
            "1. Шифр Цезаря, Виженера.",
            "2. Алгоритм шифрования RSA.",
            "3. Стеганография.",
            "4. Код Хаффмана.",
            # "5. .",
        ),
        index=3
    )

    if lab[:1] == "1":
        caesar.main()

    elif lab[:1] == "2":
        rsa.main()

    elif lab[:1] == "3":
        steganography.main()

    elif lab[:1] == "4":
        huffman.main()

    # elif lab[:1] == "5":
    #     .main()


if __name__ == "__main__":
    main()

