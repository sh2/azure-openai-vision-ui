import httpx
import os
import streamlit as st

from openai import AzureOpenAI, OpenAI
from st_img_pastebutton import paste as paste_image


def main():
    http_client = None
    openai_deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "")
    openai_proxy = os.environ.get("AZURE_OPENAI_PROXY", "")
    openai_service = os.environ.get("AZURE_OPENAI_SERVICE", "")

    if openai_proxy:
        http_client = httpx.Client(proxies={"https://": openai_proxy})

    if openai_service:
        # If the environment variable AZURE_OPENAI_SERVICE is defined, use Azure OpenAI.
        openai = AzureOpenAI(
            azure_endpoint=f"https://{openai_service}.openai.azure.com",

            # List of API versions
            # GPT-4 Turbo with Vision requires an API version of 2023-12-01-preview or later
            # https://learn.microsoft.com/en-US/azure/ai-services/openai/reference#chat-completions
            api_version=os.environ.get(
                "AZURE_OPENAI_API_VERSION") or "2024-06-01",

            api_key=os.environ.get("AZURE_OPENAI_API_KEY", ""),
            http_client=http_client
        )
    else:
        # If the environment variable AZURE_OPENAI_SERVICE is not defined, use OpenAI.
        openai = OpenAI(
            api_key=os.environ.get("AZURE_OPENAI_API_KEY", ""),
            http_client=http_client
        )

    st.title("OpenAI Vision UI")
    pasted_image = paste_image("Paste from Clipboard")

    if pasted_image:
        st.image(pasted_image)

    clear = st.button("Clear Chat History")

    if clear or "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept messages from the user
    if prompt := st.chat_input("Please enter a question about the images"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        messages_with_images = []
        response = ""

        # Display user's message
        with st.chat_message("user"):
            st.markdown(prompt)

        # For the assistant, display an empty message and update it later
        with st.chat_message("assistant"):
            message_assiatant = st.empty()

        # For the first message, change the format so that images can be attached
        messages_with_images.append({
            "role": st.session_state.messages[0]["role"],
            "content": [
                {
                    "type": "text",
                    "text": st.session_state.messages[0]["content"]
                }
            ]
        })

        # Attach images to the first message
        if pasted_image:
            messages_with_images[0]["content"].append({
                "type": "image_url",
                "image_url": {"url": pasted_image}
            })

        # Add the second and subsequent messages as they are
        for message in st.session_state.messages[1:]:
            messages_with_images.append(message)

        for response_chunk in openai.chat.completions.create(
            model=openai_deployment,
            messages=messages_with_images,
            max_tokens=4096,
            stream=True
        ):
            if response_chunk.choices:
                response += response_chunk.choices[0].delta.content or ""
                message_assiatant.markdown(response + "▌")

        message_assiatant.markdown(response)

        st.session_state.messages.append(
            {"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
