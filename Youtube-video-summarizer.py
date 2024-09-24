import os
import time
import google.generativeai as genai
from google.api_core.exceptions import InternalServerError
from youtube_transcript_api import YouTubeTranscriptApi  # For fetching YouTube transcripts
from google.generativeai.types import StopCandidateException  # Import StopCandidateException

# Configure Google GenAI API
genai.configure(api_key='AIzaSyAxpKqbnQj4PIoEAxNjNiCVUx3hjmPnIWI')

# Create the model
generation_config = {
    "temperature": 1.55,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction="Summarize the transcript of a YouTube video. Be concise, clear, and informative."
)

history = []


def get_youtube_transcript(video_id):
    """Fetch the transcript from a YouTube video."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # Combine all the text into a single string
        transcript_text = " ".join([item['text'] for item in transcript])
        return transcript_text
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None


def summarize_text(transcript):
    """Send the transcript to Google's GenAI model for summarization."""
    chat_session = model.start_chat(history=history)

    max_retries = 3  # Set the maximum number of retries
    retry_delay = 5  # Set the delay between retries in seconds

    for attempt in range(max_retries):
        try:
            response = chat_session.send_message(transcript)
            return response.text  # Get summarized text
        except StopCandidateException as e:
            # If the content violates safety policies, return a custom message
            print(f"Content flagged for safety: {e}")
            return "This content was flagged as potentially harmful and cannot be summarized."
        except (InternalServerError) as e:
            if attempt < max_retries - 1:
                print(f"{type(e)._name_} occurred. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise e  # Raise the exception if all retries fail
        except TimeoutError:
            if attempt < max_retries - 1:
                print(f"TimeoutError occurred. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise TimeoutError("Request timed out after several attempts.")


print("Welcome! Provide a YouTube video URL for summarization or type 'bye' to exit.")

while True:
    user_input = input("You: ")

    if user_input.lower() == "bye":
        print("Thank you! See you soon.")
        break

    # Check if the input is a valid YouTube URL
    if "youtube.com" in user_input or "youtu.be" in user_input:
        # Extract video ID from the YouTube URL
        if "v=" in user_input:
            video_id = user_input.split("v=")[1].split("&")[0]
        elif "youtu.be" in user_input:
            video_id = user_input.split("/")[-1]
        else:
            print("Invalid YouTube URL. Please try again.")
            continue

        # Get the transcript from the video
        transcript = get_youtube_transcript(video_id)

        if transcript:
            print("Transcript fetched successfully. Summarizing now...")
            summary = summarize_text(transcript)

            if summary:
                print('-' * 100)
                print(f'Summary:\n{summary}')
                print('-' * 100)
            else:
                print("Sorry, unable to generate the summary.")
        else:
            print("Unable to fetch the transcript for the video. Try another one.")
    else:
        print("Please enter a valid YouTube URL or type 'bye' to exit.")
