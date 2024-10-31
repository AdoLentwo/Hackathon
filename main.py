import tkinter as tk
import openai
import random

# Initialize OpenAI API key (replace 'your_api_key' with your actual key)
openai.api_key = ""

# Initialize conversation history
conversation_history = [
    {"role": "system", "content": "You are a wise and friendly ghost advisor, giving spooky yet thoughtful advice. You can become the ghost of anyone you are requested to be."}
]

def set_ghost_persona():
    # Get the user's chosen ghost
    chosen_ghost = ghost_entry.get()

    # Generate response from OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        answer = response['choices'][0]['message']['content']
        
        # Append the ghost's response to the conversation history
        conversation_history.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        answer = f"The ghost is silent... (Error: {e})"
    
    persona = f"You are the ghost of {chosen_ghost}, known for wisdom and unique perspectives. Speak thoughtfully and mystically."
    
    # Add persona to the conversation history
    conversation_history.append({"role": "system", "content": persona})

def ghost_response():
    user_input = user_entry.get()
    
    # Append the user's message to the conversation history
    conversation_history.append({"role": "user", "content": user_input})

    # Generate response from OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        answer = response['choices'][0]['message']['content']
        
        # Append the ghost's response to the conversation history
        conversation_history.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        answer = f"The ghost is silent... (Error: {e})"
    
    # Display the ghost's response in the main window
    ghost_response_label.config(text=answer)

def flicker_background():
    # Randomly choose between a few shades to simulate flickering
    colors = ["#0f0f0f", "#1a1a1a", "#222222", "#000000"]
    current_color = random.choice(colors)
    window.configure(bg=current_color)
    ghost_response_label.configure(bg=current_color)
    label.configure(bg=current_color)
    ask_button.configure(bg="grey")  # Reset button color
    user_entry.configure(bg="#333333")
    
    # Continue flickering every 500 ms
    window.after(500, flicker_background)

# Create the main Tkinter window
window = tk.Tk()
window.title("Ask the Ghost")

# Window styling
window.geometry("400x400")
window.configure(bg="black")

# Create spooky label and entry
label = tk.Label(window, text="Ask the ghost a question:", font=("Helvetica", 14), fg="white", bg="black")
label.pack(pady=20)

user_entry = tk.Entry(window, width=40, font=("Helvetica", 12), bg="#333333", fg="white")
user_entry.pack()

# Add Ask button
ask_button = tk.Button(window, text="Ask", command=ghost_response, bg="grey", fg="black")
ask_button.pack(pady=20)

# Label to display the ghost's response
ghost_response_label = tk.Label(window, text="", font=("Helvetica", 12, "italic"), fg="#90EE90", bg="black", wraplength=350)
ghost_response_label.pack(pady=20)

# Start the flickering effect
flicker_background()

# Run the GUI event loop
