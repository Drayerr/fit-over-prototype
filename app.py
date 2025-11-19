import streamlit as st
import os
from dotenv import load_dotenv
import replicate

load_dotenv()

st.set_page_config(page_title="FitOver - Virtual Try-On", layout="wide")

st.title("👕 FitOver: Your AI Virtual Try-On")
st.write("Prototype v0.1")

api_token = os.getenv("REPLICATE_API_TOKEN")
if api_token:
    st.success("API Key detected! System ready to connect.")
else:
    st.warning("API Key not found. Please configure the .env file.")

col1, col2 = st.columns(2)

with col1:
    st.header("1 - Your photo")
    user_photo_file = st.file_uploader(
        "Upload your photo", type=["jpg", "png", "jpeg"], key="user_photo"
    )

    if user_photo_file is not None:
        st.subheader("Preview:")
        st.image(user_photo_file, caption="Your photo", use_container_width=True)

with col2:
    st.header("2 - Clothing photo")
    clothing_file = st.file_uploader(
        "Upload the clothing photo", type=["jpg", "png", "jpeg"], key="clothing_photo"
    )

    if clothing_file is not None:
        st.subheader("Preview:")
        st.image(clothing_file, caption="Clothing photo", use_container_width=True)


is_ready = user_photo_file is not None and clothing_file is not None

st.markdown("---")
if st.button(
    "Run Script", disabled=not is_ready, type="primary", use_container_width=True
):
    if user_photo_file and clothing_file:
        try:
            input = {
                "model_image": user_photo_file,
                "top_image": clothing_file,
            }

            output = replicate.run("omnious/vella-1.5", input=input)

            if output and isinstance(output, list) and len(output) > 0:

                result_url = getattr(output[0], "url", None)

                if result_url:
                    st.session_state["result_url"] = result_url
                    st.success("Generation complete!")
                    print("$$RESULT$$", result_url)
                else:
                    st.error("Model returned an unexpected result or no URL.")
                    st.session_state["result_url"] = None
            else:
                st.error("Model returned an empty or invalid output.")
                st.session_state["result_url"] = None

        except Exception as e:
            st.error(f"An error occurred during API call: {e}")
            st.session_state["result_url"] = None


st.markdown("---")

if "result_url" in st.session_state and st.session_state["result_url"]:
    st.subheader("Final Result: ")
    st.image(
        st.session_state["result_url"],
        caption="Try-On Result",
        use_container_width=True,
    )

    st.link_button(
        "Download Result",
        st.session_state["result_url"],
        type="primary",
        use_container_width=True,
    )
else:
    st.info("Upload your photos and click 'Run Virtual Try-On' to generate the result.")
