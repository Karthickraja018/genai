import google.generativeai as genai
import gradio as gr

# Configure Google API key directly
API_KEY = "AIzaSyCoFw6Vl7R6GHgcI616K5ulsn15xa6tR0o"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# Load the Gemini model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


# Function to get response from Gemini
def get_gemini_response(input_text, uploaded_image, prompt):
    try:
        response = model.generate_content([prompt, uploaded_image, input_text])
        return response.text
    except Exception as e:
        return f"Error in Gemini response: {str(e)}"


# Define the Gradio interface components
def bs_extractor(input_text, uploaded_image):
    prompt = """
         You are an expert in understanding bank statements. We will upload an image of a bank statement, 
         and you will have to answer any questions based on the uploaded bank statement.
     """
    if input_text and uploaded_image is not None:
        return get_gemini_response(input_text, uploaded_image, prompt)
    else:
        return "Please provide both an input prompt and an image."


# Gradio Interface
iface = gr.Interface(
    fn=bs_extractor,
    inputs=[
        gr.Textbox(label="Input Prompt"),
        gr.Image(type="pil", label="Upload a Bank Statement Image"),
    ],
    outputs="text",
    title="BS Extractor",
    description="Upload a bank statement image and enter a prompt. The system will analyze the statement."
)

# Launch the interface
if _name_ == "_main_":
    iface.launch()
