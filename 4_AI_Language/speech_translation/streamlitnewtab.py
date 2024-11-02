import streamlit as st

st.title('新しいタブでGoogleを開くボタン')

# ボタンを作成
if st.button('Googleを新しいタブで開く'):
    # HTMLのリンクを表示して新しいタブでGoogleを開く
    st.write('[Googleを新しいタブで開く](https://www.google.com)', unsafe_allow_html=True)