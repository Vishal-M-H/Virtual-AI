import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice")

# Function to convert text to audio and save as a file
async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3"

    # If the file already exists, delete it
    if os.path.exists(file_path):
        os.remove(file_path)

    # Generate speech from the text and save it to the file
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
    await communicate.save(r'Data\speech.mp3')

# Function to handle Text-to-Speech (TTS)
def TTS(Text, func=lambda r=None: True):
    while True:
        try:
            # Call the async function to convert text to audio
            asyncio.run(TextToAudioFile(Text))

            # Initialize pygame mixer to play the audio
            pygame.mixer.init()
            pygame.mixer.music.load(r"Data\speech.mp3")
            pygame.mixer.music.play()

            # Keep the program running while audio is playing
            while pygame.mixer.music.get_busy():
                if func() == False:
                    break
                pygame.time.Clock().tick(10)

            return True
        
        except Exception as e:
            print(f"Error in TTS: {e}")

        finally:
            try:
                # Stop music and quit pygame mixer
                func(False)
                pygame.mixer.music.stop()
                pygame.mixer.quit()

            except Exception as e:
                print(f"Error in finally block: {e}")

# Function to split and process the text, calling TTS
def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".")

    # Define a set of responses to choose from
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    # If the length of the data is large, use a response with part of the text
    if len(Data) > 4 and len(Text) >= 250:
        TTS(" ".join(Text.split(".")[0:2]) + ". " + random.choice(responses), func)
    else:
        TTS(Text, func)

# Main function to run the text-to-speech program
if __name__ == "__main__":
    while True:
        TextToSpeech(input("Enter the text: "))

        


    