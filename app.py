import streamlit as st
import os
from dotenv import load_dotenv
import replicate
from streamlit_extras.stylable_container import stylable_container

load_dotenv()


def add_footer():
    st.markdown(
        """
        <style>
        .footer {
            left: 0;
            bottom: 0;
            height: 40px;
            width: 100%;
            background-color: "transparent";
            color: #555555;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            z-index: 100;
        }
        </style>
        <div class="footer">
            <p>FitOver by Gabriel Ribeiro | Prototype v0.2 &copy; 2025</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(page_title="FitOver - Virtual Try-On", layout="wide")

m_left, content, m_right = st.columns([0.2, 1, 0.2])

with content:
    st.title("👕 FitOver: Your AI Virtual Try-On")
    st.write("Prototype v0.2")

    api_token = os.getenv("REPLICATE_API_TOKEN")
    if api_token:
        st.success("API Key detected!", width=150)
    else:
        st.warning("API Key not found. Please configure the .env file.", width=360)

    col1, col_gap, col2 = st.columns([1, 0.2, 1])

    with col1:
        st.header("1 - Your photo")
        user_photo_file = st.file_uploader(
            "Upload your photo",
            type=["jpg", "png", "jpeg"],
            key="user_photo",
        )

        if user_photo_file is not None:
            with stylable_container(
                key="user_image_container",
                css_styles="""
                    img {
                        width: 250px !important; 
                        height: 250px !important; 
                        object-fit: cover;
                    }
                """,
            ):
                st.image(
                    user_photo_file, caption="Your photo", use_container_width=True
                )

    with col2:
        st.header("2 - Clothing photo")
        clothing_file = st.file_uploader(
            "Upload the clothing photo",
            type=["jpg", "png", "jpeg"],
            key="clothing_photo",
        )

        if clothing_file is not None:
            with stylable_container(
                key="clothing_image_container",
                css_styles="""
                    img {
                        width: 250px !important; 
                        height: 250px !important; 
                        object-fit: cover;
                    }
                """,
            ):
                st.image(
                    clothing_file, caption="Clothing photo", use_container_width=True
                )

    is_ready = user_photo_file is not None and clothing_file is not None

    st.markdown("---")

    with stylable_container(
        "Green",
        css_styles="""
        button {
            background-color: #1f9939;
        }""",
    ):
        run_button = st.button(
            "Run Script",
            key="button2",
            disabled=not is_ready,
            use_container_width=False,
        )

    if run_button:
        if user_photo_file and clothing_file:
            with st.spinner(
                "Processing... Uploading images and running AI model (may take 30-60 seconds)."
            ):
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
        st.info("Upload your photos and click 'Run Script' to generate the result.")

    st.markdown("---")

add_footer()
