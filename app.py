import streamlit as st
import pandas as pd
from PIL import Image
import requests

# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

# Function to get sentences from database (placeholder)
def get_sentences_from_db():
    # Replace this with actual database query
    return [
        "The government should increase funding for education.",
        "Healthcare should be a universal right.",
        "Climate change is a pressing issue that needs immediate action.",
        "The tax system should be reformed to reduce income inequality.",
        "Immigration policies should be more lenient."
    ]

# Function to get candidate information (placeholder)
def get_candidate_info(level):
    # Replace this with actual database query
    return {
        'agree': [
            {'name': 'John Doe', 'photo': 'https://example.com/johndoe.jpg'},
            {'name': 'Jane Smith', 'photo': 'https://example.com/janesmith.jpg'},
        ],
        'disagree': [
            {'name': 'Bob Johnson', 'photo': 'https://example.com/bobjohnson.jpg'},
            {'name': 'Alice Brown', 'photo': 'https://example.com/alicebrown.jpg'},
        ]
    }

# Main app
def main():
    st.title("Based Logic: US Election Insight")

    # User input
    zipcode = st.text_input("Enter your Zipcode")
    gender = st.selectbox("Select your Gender", ["Male", "Female", "Other"])
    dob = st.date_input("Enter your Date of Birth")

    if zipcode and gender and dob:
        sentences = get_sentences_from_db()

        # Create a glossy white container
        container = st.container()
        container.markdown(
            f"""
            <style>
            .glossy-container {{
                background: linear-gradient(to bottom, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0.9) 100%);
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }}
            .centered-text {{
                text-align: center;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
                color: #333;
            }}
            .button-container {{
                display: flex;
                justify-content: center;
                gap: 10px;
            }}
            .stButton > button {{
                border-radius: 5px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.3);
                font-size: 18px;
                padding: 10px 20px;
                transition: all 0.3s ease;
            }}
            .stButton > button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            }}
            .agree-button > button {{
                background: linear-gradient(to bottom, #4CAF50, #45a049);
                color: white;
            }}
            .neutral-button > button {{
                background: linear-gradient(to bottom, #FFD700, #FFC700);
                color: black;
            }}
            .disagree-button > button {{
                background: linear-gradient(to bottom, #f44336, #d32f2f);
                color: white;
            }}
            </style>
            <div class="glossy-container">
                <div class="centered-text">{sentences[st.session_state.current_question]}</div>
                <div class="button-container">
                    <div id="agree-button"></div>
                    <div id="neutral-button"></div>
                    <div id="disagree-button"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Place buttons in the designated areas
        agree_button = container.empty()
        neutral_button = container.empty()
        disagree_button = container.empty()

        agree_clicked = agree_button.button("Agree", key="agree", help="Click if you agree with the statement")
        neutral_clicked = neutral_button.button("Neutral", key="neutral", help="Click if you're neutral about the statement")
        disagree_clicked = disagree_button.button("Disagree", key="disagree", help="Click if you disagree with the statement")

        if agree_clicked or neutral_clicked or disagree_clicked:
            if agree_clicked:
                st.session_state.answers.append("Agree")
            elif neutral_clicked:
                st.session_state.answers.append("Neutral")
            else:
                st.session_state.answers.append("Disagree")
            
            # Save answer to database (placeholder)
            save_answer_to_db(st.session_state.current_question, st.session_state.answers[-1])
            
            st.session_state.current_question += 1
            if st.session_state.current_question >= len(sentences):
                st.session_state.current_question = 0
            st.experimental_rerun()

        # Display candidate results after 5 questions
        if len(st.session_state.answers) >= 5:
            st.markdown(
                """
                <style>
                .results-container {
                    background: linear-gradient(to bottom, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0.9) 100%);
                    border-radius: 10px;
                    padding: 20px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    margin-top: 20px;
                }
                </style>
                <div class="results-container">
                    <h2>Candidate Results</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

            tab1, tab2, tab3 = st.tabs(["Local", "State", "Federal"])

            for tab, level in zip([tab1, tab2, tab3], ["local", "state", "federal"]):
                with tab:
                    candidates = get_candidate_info(level)
                    agree, disagree = st.columns(2)

                    with agree:
                        st.subheader("Candidates you may agree with")
                        for candidate in candidates['agree']:
                            st.write(candidate['name'])
                            st.image(candidate['photo'], width=100)

                    with disagree:
                        st.subheader("Candidates you may disagree with")
                        for candidate in candidates['disagree']:
                            st.write(candidate['name'])
                            st.image(candidate['photo'], width=100)

def save_answer_to_db(question_index, answer):
    # Replace this with actual database save operation
    print(f"Saving answer: Question {question_index + 1}, Answer: {answer}")
if __name__ == "__main__":
    main()