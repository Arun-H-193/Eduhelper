import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="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")

# Function for text-to-audio generation with OpenAI TTS API
def generate_audio_from_text(text):
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="echo",
            input=text
        )
        return response.content
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None

def summarize_text(text, max_tokens=1000):
    try:
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=text,
            max_tokens=max_tokens,
            temperature=0.5
        )
        return response.choices[0].text
    except Exception as e:
        print(f"Error summarizing text: {e}")
        return None

# Inside the generate_story_and_audio function
def generate_story_and_audio(user_prompt, difficulty_level, story_length, tone, genre):
    try:
        # Modify the prompt based on user-selected options
        prompt_options = f"Write a {tone} story of difficulty level {difficulty_level}/10 in the {genre} genre: {user_prompt}"
        prompt_with_options = f"{prompt_options} Limit the story to {story_length} words."

        # Generate story using OpenAI GPT-3.5-turbo-instruct engine
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt_with_options,
            max_tokens=1000
        )

        # Store the generated story in session state
        st.session_state.generated_story = response.choices[0].text

        # Display the generated story with title
        st.subheader(f"**{user_input_title}**")
        st.write(response.choices[0].text)

        # Generate audio from the generated story
        audio_content = generate_audio_from_text(response.choices[0].text)

        if audio_content:
            # Display the audio player
            st.subheader("Generated Audio:")
            st.audio(audio_content, format="audio/mp3", start_time=0)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Streamlit UI
st.title("EduHelper.ai Story Generator")
st.markdown("Customize your storytelling experience. Enter a prompt, select options, and click 'Generate Story' to see the magic!")

# User input for prompt and story title
user_input_prompt = st.text_area("Write a prompt for the AI storyteller:")
user_input_title = st.text_input("Enter a title for the story:")

# User input for difficulty level
difficulty_level = st.slider("Select difficulty level:", min_value=1, max_value=10, value=5)

# User input for story customization
story_length = st.number_input("Limit the story length (words):", min_value=10, max_value=1000, value=500)
tone = st.selectbox("Select tone:", ["Happy", "Sad", "Suspenseful"], index=0)
genre = st.selectbox("Select genre:", ["Fantasy", "Sci-Fi", "Mystery"], index=0)

# Button to generate the story, audio, and other components
if st.button("Generate Story"):
    if user_input_prompt:
        generate_story_and_audio(user_input_prompt, difficulty_level, story_length, tone, genre)
    else:
        st.warning("Please enter a prompt for the AI storyteller.")
