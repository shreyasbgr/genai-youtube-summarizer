import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv() # Load all the environment variables
import os
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
input_prompt = """
You are a Youtube video summarizer. You will be taking the
transcript text and summarizing the entire video and providing the
important details of the video as a summary, using points wherever possible. The transcript text is as follows:

"""
def generate_gemini_content(transcript_text,input_prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(input_prompt + transcript_text)
    return response.text

# Use youtube_transcript_api to take a youtube video url and get it's transcript
def fetch_transcript_details(youtube_url):
    try:
        video_id = youtube_url.split("v=")[-1]
        
        # Attempt to fetch the transcript in English first
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        except NoTranscriptFound:
            # If English transcript is not found, attempt to fetch the Hindi transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi'])

        transcript_text = " ".join([entry["text"] for entry in transcript])
        return transcript_text
    
    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."
    except NoTranscriptFound:
        return "No transcript available for the video in the requested languages."
    except Exception as e:
        return f"Error fetching transcript: {e}"

st.set_page_config(page_title="Youtube Video Summarizer")
st.subheader("Youtube Video Summarizer")
youtube_link = st.text_input("Enter the Youtube Video Link")

if youtube_link:
    video_id = youtube_link.split("=")[-1]
    # Display the video thumbnail
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
    

    if st.button("Get Summary"):
        transcript_text = fetch_transcript_details(youtube_link)
        if transcript_text:
            summary = generate_gemini_content(transcript_text, input_prompt)
            st.markdown("## Summary of the Youtube video")
            st.write(summary)