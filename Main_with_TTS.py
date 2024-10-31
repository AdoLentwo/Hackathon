import tkinter as tk
import openai
import random
import requests
import pygame
###
'''
small read me section here, use pip install pygame and pip install elevenlabs in cmd to get the packages for the TTS. 
'''
###
# Initialize OpenAI and ElevenLabs API keys
openai.api_key = ""  # Replace with your OpenAI API key
api_key = ''  # Replace with your ElevenLabs API key
# Conversation history for OpenAI API
conversation_history = [
    {
        "role": "system",
        "content": "You are a wise and friendly ghost advisor, giving spooky yet thoughtful advice. You can become the ghost of anyone you are requested to be."
    }
]

# Function to generate speech with ElevenLabs API and play it immediately

def generate_speech(text, voice_id="Dz5ybcCvrahl9DAD0yAG", output_filename="output.mp3"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.2,
            "similarity_boost": 0.9
        }
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        # Save the audio content to a file
        with open(output_filename, "wb") as file:
            file.write(response.content)
        print(f"Audio saved as {output_filename}")
        
        # Play the audio file
        pygame.mixer.init()  # Initialize the mixer
        pygame.mixer.music.load(output_filename)  # Load the mp3 file
        pygame.mixer.music.play()  # Play the audio
    else:
        print("Error:", response.status_code, response.text)

# Function to set the ghost's persona based on user input
def set_ghost_persona():
    chosen_ghost = ghost_entry.get()
    persona = f"You are the ghost of {chosen_ghost}, known for wisdom and unique perspectives. Speak thoughtfully and mystically."
    conversation_history.append({"role": "system", "content": persona})

# Function to get the ghost's response based on user input
def ghost_response():
    user_input = user_entry.get()
    conversation_history.append({"role": "user", "content": user_input})
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        answer = response['choices'][0]['message']['content']
        conversation_history.append({"role": "assistant", "content": answer})

        # Generate speech with the assistant's response
        generate_speech(text=answer, voice_id="Dz5ybcCvrahl9DAD0yAG", output_filename="output.mp3")

    except Exception as e:
        answer = f"The ghost is silent... (Error: {e})"
    
    ghost_response_label.config(text=answer)

# Function to create a flickering background effect
def flicker_background():
    colors = ["#0f0f0f", "#1a1a1a", "#222222", "#000000"]
    current_color = random.choice(colors)
    window.configure(bg=current_color)
    ghost_response_label.configure(bg=current_color)
    label.configure(bg=current_color)
    ask_button.configure(bg="grey")
    user_entry.configure(bg="#333333")
    window.after(500, flicker_background)

# Initialize the Tkinter GUI
window = tk.Tk()
window.title("Ask the Ghost")
window.geometry("400x400")
window.configure(bg="black")

# Create and pack widgets
label = tk.Label(window, text="Ask the ghost a question:", font=("Helvetica", 14), fg="white", bg="black")
label.pack(pady=20)

user_entry = tk.Entry(window, width=40, font=("Helvetica", 12), bg="#333333", fg="white")
user_entry.pack()

ask_button = tk.Button(window, text="Ask", command=ghost_response, bg="grey", fg="black")
ask_button.pack(pady=20)

ghost_response_label = tk.Label(window, text="", font=("Helvetica", 12, "italic"), fg="#90EE90", bg="black", wraplength=350)
ghost_response_label.pack(pady=20)

# Start flickering effect
flicker_background()

# Run the GUI event loop
window.mainloop()