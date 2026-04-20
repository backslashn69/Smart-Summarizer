import streamlit as st
from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("Smartly shortened Summarizer")
st.write("Enter text to summarize")

text = st.text_area("Enter text here", height=200)

mode = st.selectbox("Select summarization style", ["Quick Summary", "Detailed Summary", "Bullet Points"])

if st.button("Summarize"):
    if text:
        word_count_before = len(text.split())

        if mode == "Quick Summary":
            prompt = f"Summarize the text in 2-3 sentences: {text}"
        elif mode == "Detailed Summary":
            prompt = f"Summarize the text in detail, covering all key points: {text}"
        elif mode == "Bullet Points":
            prompt = f"List the key points from the text as bullet points: {text}"

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
               {"role": "user", "content": prompt}
            ]
        )

        summary = response.choices[0].message.content
        word_count_after = len(summary.split())
        reduction = round (1- word_count_after / word_count_before) * 100

        st.subheader("Summary:")
        st.write(summary)

        st.divider()
        col1, col2, col3 = st.columns(3)
        col1.metric("Original Word Count", word_count_before)
        col2.metric("Summary Word Count", word_count_after)
        col3.metric("Reduced by", f"{reduction}%")
    else:
        st.warning("Please enter some text to summarize.")
