import streamlit as st

from lab_01 import caesar
# from lab_02 import
# from lab_03 import
# from lab_04 import
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
            "1. Шифр Цезаря. Шифр Виженера.",
            # "2. .",
            # "3. .",
            # "4. .",
            # "5. .",
        ),
        index=0
    )

    if lab[:1] == "1":
        caesar.main()

    # elif lab[:1] == "2":
    #     .main()
    #
    # elif lab[:1] == "3":
    #     .main()
    #
    # elif lab[:1] == "4":
    #     .main()
    #
    # elif lab[:1] == "5":
    #     .main()


if __name__ == "__main__":
    main()

