import streamlit as st
from openai import OpenAI

# Ask the user to input their OpenAI API key
api_key = st.text_input("Enter your OpenAI API Key:", type="password")

# Only proceed if the API key is provided
if api_key:
    client = OpenAI(api_key=api_key)

    # Function to generate a response based on user's emotion
    def generate_response(emotion, follow_up=None):
        if follow_up:
            messages = [
                {"role": "user", "content": f"I am feeling {emotion} today."},
                {"role": "assistant", "content": f"I understand you're feeling {emotion}. Can you tell me more about what's causing this feeling?"},
                {"role": "user", "content": follow_up},
                {"role": "system", "content": "You are a compassionate therapist. Based on the user's emotion and their explanation, provide a supportive response and suggest a coping strategy."}
            ]
        else:
            messages = [
                {"role": "system", "content": "You are a compassionate therapist. Respond to the user's emotion with empathy."},
                {"role": "user", "content": f"I am feeling {emotion} today."}
            ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content.strip()

    # Streamlit app layout
    st.title("Therapy Bot")

    # Ask the user how they are feeling today
    st.subheader("How are you feeling today?")

    # List of emotions to choose from
    emotions = [
        "Happy", "Sad", "Angry", "Anxious", "Excited", "Lonely", "Stressed",
        "Confused", "Motivated", "Relaxed", "Overwhelmed", "Hopeful", "Frustrated"
    ]

    # Negative emotions that require follow-up
    negative_emotions = ["Sad", "Angry", "Anxious", "Lonely", "Stressed", "Overwhelmed", "Frustrated"]

    # User selects an emotion
    selected_emotion = st.selectbox("Select an emotion", emotions)

    # Initialize session state for conversation
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

    # Button to submit the emotion
    if st.button("Submit"):
        # Generate initial response
        initial_response = generate_response(selected_emotion)
        st.session_state.conversation.append(("Therapist", initial_response))

        # If it's a negative emotion, ask for more details
        if selected_emotion in negative_emotions:
            st.session_state.conversation.append(("Therapist", f"Can you tell me more about why you're feeling {selected_emotion.lower()}?"))

    # Display conversation
    for role, message in st.session_state.conversation:
        st.markdown(f"**{role}:** {message}")

    # If the last message was from the therapist asking for more details, show an input field
    if st.session_state.conversation and st.session_state.conversation[-1][0] == "Therapist" and "Can you tell me more" in st.session_state.conversation[-1][1]:
        user_input = st.text_input("Your response:")
        if st.button("Send"):
            st.session_state.conversation.append(("You", user_input))
            follow_up_response = generate_response(selected_emotion, user_input)
            st.session_state.conversation.append(("Therapist", follow_up_response))
            st.experimental_rerun()

    # Additional features
    st.markdown("---")
    st.markdown("This chatbot is here to help you reflect on your emotions and guide you toward a better mindset. Remember, professional therapy is always recommended for serious emotional concerns.")

    # Add a reset button to clear the conversation
    if st.button("Start Over"):
        st.session_state.conversation = []
        st.experimental_rerun()

else:
    st.warning("Please enter your OpenAI API key to use the chatbot.")

# Add some information about the app
st.sidebar.title("About")
st.sidebar.info(
    "This Therapy Chatbot uses AI to provide supportive responses based on your emotional state. "
    "It's designed to offer a listening ear and gentle guidance. "
    "Remember, while this can be a helpful tool for reflection, it's not a substitute for professional mental health support."
)

# Add a disclaimer
st.sidebar.title("Disclaimer")
st.sidebar.warning(
    "This chatbot is for informational purposes only and is not a substitute for professional medical advice, "
    "diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider "
    "with any questions you may have regarding a medical condition."
)
