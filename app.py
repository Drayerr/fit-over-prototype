import streamlit as st
import os
from dotenv import load_dotenv
import replicate
from streamlit_extras.stylable_container import stylable_container
import requests
from streamlit_image_select import image_select

st.markdown(
    """
        <style>
            [data-testid='stFileUploader'] section {
                background-color: transparent;
                border: none;
                padding-top: 0;
                min-height: 0;
                margin: 0;
            }

            [data-testid='stFileUploader'] section > input + div {
                display: none;
            }
            
            [data-testid='stFileUploader'] section button {
                margin: 0;
                /* width: 100%; */
            }
        </style>
    """,
    unsafe_allow_html=True,
)


load_dotenv()


def search_google_images(query, api_key, cx_id, num_results=4):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "cx": cx_id,
        "key": api_key,
        "searchType": "image",
        "num": num_results,
        "safe": "active",
        "fileType": "jpg,png",
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        search_results = response.json()
        image_links = [item["link"] for item in search_results.get("items", [])]
        return image_links
    except Exception as e:
        st.error(f"Searching error: {e}")
        return []


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
            <p>FitOver by Gabriel Ribeiro | Prototype v0.3 &copy; 2025</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(page_title="FitOver - Virtual Try-On", layout="wide")


m_left, content, m_right = st.columns([0.1, 1, 0.1])

with content:
    st.title("👕 FitOver: Your AI Virtual Try-On")
    st.write("Prototype v0.3")

    api_token = os.getenv("REPLICATE_API_TOKEN")
    api_google_search = os.getenv("GOOGLE_SEARCH_API")
    search_engine_id = os.getenv("SEARCH_ENGINE_ID")

    if api_token:
        st.success("API Key detected!", width=150)
    else:
        st.warning("API Key not found. Please configure the .env file.", width=360)

    col1, col_gap, col2, col_gap2, col3 = st.columns([1, 0.1, 1, 0.1, 1])

    with col1:
        st.header("1 - Search for Clothing")
        search_query = st.text_input(
            "",
            key="tshirt_search",
            label_visibility="collapsed",
            placeholder="What kind of clothing do you have in mind?",
        )
        search_button = st.button("Search Google Images")

        if "search_results" not in st.session_state:
            st.session_state["search_results"] = []
        if "selected_image_url" not in st.session_state:
            st.session_state["selected_image_url"] = None

        if search_button:
            if not search_query:
                st.warning("Please enter a search term.")
            elif not api_google_search or not search_engine_id:
                st.error("Google API or Search Engine ID not found in ENV file.")
            else:
                with st.spinner("Searching Google Images..."):
                    results = search_google_images(
                        search_query, api_google_search, search_engine_id
                    )
                    if results:
                        st.session_state["search_results"] = results
                        st.session_state["selected_image_url"] = None
                    else:
                        st.warning("No images found.")

        if st.session_state["search_results"]:
            selected_url = image_select(
                label="Click to select:",
                images=st.session_state["search_results"],
                use_container_width=False,
                return_value="original",
                index=-1,
            )

            if selected_url:
                st.session_state["selected_image_url"] = selected_url

    with col2:
        st.header("2 - Upload your photo")
        user_photo_file = st.file_uploader(
            label="Upload your photo",
            type=["jpg", "png", "jpeg"],
            key="user_photo",
            label_visibility="collapsed",
        )

        if user_photo_file is not None:
            with stylable_container(
                key="user_image_container",
                css_styles="""
                    img {
                        width: 300px !important; 
                        height: 300px !important; 
                        object-fit: cover;
                    }
                """,
            ):
                st.image(user_photo_file, use_container_width=True)

    has_selected_image = st.session_state.get("selected_image_url") is not None
    has_user_photo = user_photo_file is not None

    is_ready = has_user_photo and has_selected_image

    with stylable_container(
        "Green",
        css_styles="""
        button {
            background-color: #1f9939;
        }""",
    ):
        run_button = st.button(
            "Run Script",
            key="run-script-button",
            disabled=not is_ready,
            use_container_width=False,
        )

    with col3:

        if run_button:
            if user_photo_file and st.session_state["selected_image_url"]:
                with st.spinner(
                    "Processing... Uploading images and running AI model (may take 30-60 seconds)."
                ):
                    try:
                        input = {
                            "model_image": user_photo_file,
                            "top_image": st.session_state["selected_image_url"],
                        }

                        output = replicate.run("omnious/vella-1.5", input=input)

                        if output and isinstance(output, list) and len(output) > 0:

                            result_url = getattr(output[0], "url", None)

                            if result_url:
                                st.session_state["result_url"] = result_url
                            else:
                                st.error(
                                    "Model returned an unexpected result or no URL."
                                )
                                st.session_state["result_url"] = None
                        else:
                            st.error("Model returned an empty or invalid output.")
                            st.session_state["result_url"] = None

                    except Exception as e:
                        st.error(f"An error occurred during API call: {e}")
                        st.session_state["result_url"] = None

        st.header("Final Result: ")

        if "result_url" in st.session_state and st.session_state["result_url"]:
            st.success("Generation complete!")
            st.caption("Generated with omnious/vella-1.5")
            with stylable_container(
                key="result_image_container",
                css_styles="""
                            img {
                                width: 400px !important;
                                height: 450px !important;
                                margin-bottom: 16px;
                                object-fit: cover;
                            }
                        """,
            ):
                st.image(
                    st.session_state["result_url"],
                    caption="",
                    use_container_width=True,
                )

            with stylable_container(
                "Download-Button",
                css_styles="""
                a {
                    background-color: #1887db;
                }""",
            ):
                st.link_button(
                    "Download Result",
                    st.session_state["result_url"],
                    use_container_width=True,
                )
        else:
            st.info(
                "Select a clothing item and upload your photo to generate the result."
            )

    st.markdown("---")


add_footer()
