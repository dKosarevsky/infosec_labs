import streamlit as st
import pandas as pd
from collections import Counter


class Node:
    def __init__(self, prob, symbol, left=None, right=None):
        self.prob = prob

        self.symbol = symbol

        self.left = left

        self.right = right

        self.code = ""


codes = dict()


def calculate_codes(node, val=""):
    new_val = val + str(node.code)

    if node.left:
        calculate_codes(node.left, new_val)
    if node.right:
        calculate_codes(node.right, new_val)
    if not node.left and not node.right:
        codes[node.symbol] = new_val

    return codes


def calculate_probability(data):
    symbols = dict()
    for element in data:
        if symbols.get(element) is None:
            symbols[element] = 1
        else:
            symbols[element] += 1
    return symbols


def output_encoded(data, coding):
    encoding_output = []
    for c in data:
        encoding_output.append(coding[c])

    string = "".join([str(item) for item in encoding_output])
    return string


def total_gain(data, coding):
    before_compression = len(data) * 8
    after_compression = 0
    symbols = coding.keys()
    for symbol in symbols:
        count = data.count(symbol)
        after_compression += count * len(coding[symbol])
    return before_compression, after_compression


def encoding(data):
    symbol_with_probs = calculate_probability(data)
    symbols = symbol_with_probs.keys()
    st.write("Символы: ", symbols)

    nodes = []

    for symbol in symbols:
        nodes.append(Node(symbol_with_probs.get(symbol), symbol))

    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.prob)

        right = nodes[0]
        left = nodes[1]

        left.code = 0
        right.code = 1

        new_node = Node(left.prob + right.prob, left.symbol + right.symbol, left, right)

        nodes.remove(left)
        nodes.remove(right)
        nodes.append(new_node)

    encoding_res = calculate_codes(nodes[0])

    freq = pd.DataFrame.from_dict(dict(Counter(data)), orient="index", columns=["Частота"])
    df = pd.DataFrame.from_dict(encoding_res, orient="index", columns=["Код"])
    merged_df = freq.merge(df, left_index=True, right_index=True).sort_values(by="Частота")
    st.write("Символы с частотой и кодами:", merged_df)

    before, after = total_gain(data, encoding_res)
    encoded_output = output_encoded(data, encoding_res)

    return encoded_output, nodes[0], before, after


def decoding(encoded_data, huffman_tree):
    tree_head = huffman_tree
    decoded_output = []
    for x in encoded_data:
        if x == "1":
            huffman_tree = huffman_tree.right
        elif x == "0":
            huffman_tree = huffman_tree.left
        try:
            if huffman_tree.left.symbol is None and huffman_tree.right.symbol is None:
                pass
        except AttributeError:
            decoded_output.append(huffman_tree.symbol)
            huffman_tree = tree_head

    string = "".join([str(item) for item in decoded_output])
    return string


def main():
    st.markdown("### Лабораторная работа №4")
    st.markdown("**Тема:** Код Хаффмана")
    st.markdown("""
        **Алгоритм Хаффмана** 
    — жадный алгоритм оптимального префиксного кодирования алфавита с минимальной избыточностью. 
    Был разработан в 1952 году аспирантом Массачусетского технологического института Дэвидом Хаффманом 
    при написании им курсовой работы. В настоящее время используется во многих программах сжатия данных.
    """)
    st.markdown("---")

    with st.form("encoding"):
        message = st.text_area(
            "Введите сообщение для сжатия:",
            value="beep boop beer!"
        )
        st.form_submit_button("Кодировать")
        encoded, tree, size_before, size_after = encoding(message)
        st.write("Результат сжатия:")
        st.code(encoded)
        st.write("Размер до сжатия (биты):", size_before)
        st.write("Размер после сжатия (биты):", size_after)

    with st.form("decoding"):
        st.form_submit_button("Декодировать")
        decoded = decoding(encoded, tree)
        st.write(decoded)


if __name__ == "__main__":
    main()
