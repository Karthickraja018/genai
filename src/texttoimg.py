import streamlit as st
import google.generativeai as genai

# Directly use the API key (not recommended for production)
API_KEY = "AIzaSyCoFw6Vl7R6GHgcI616K5ulsn15xa6tR0o"

# Configure the Gemini API
genai.configure(api_key=API_KEY)

# Streamlit interface for text input and image output
st.title("Text-to-Image Generator using Gemini API")

# Input field for user to enter a text prompt
prompt = st.text_input("Enter a text prompt for the image:")

# When the user presses the "Generate Image" button
if st.button("Generate Image"):
    if prompt:
        try:
            # Generate the image using Gemini
            model = genai.GenerativeModel('gemini-pro-vision')
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    candidate_count=1,
                    max_output_tokens=2048,
                )
            )
            
            # Check if the response contains an image
            if response.parts:
                for part in response.parts:
                    if hasattr(part, 'image'):
                        st.image(part.image.url, caption=f"Generated from prompt: {prompt}")
                        break
                else:
                    st.error("No image was generated in the response.")
            else:
                st.error("The response did not contain any parts.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please enter a text prompt.")
