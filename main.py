import json
import datetime
from tzlocal import get_localzone
from json.decoder import JSONDecodeError
from transformers import MarianMTModel, MarianTokenizer
from langdetect import detect

class ConversationTranslator:
    """
    A conversational translator class that allows users to register, chat, and translate messages.
    Keeps track of user profiles and translation history.
    """

    def __init__(self):
        """
        Initializes a new ConversationTranslator instance.
        Loads user profiles and initializes an empty translation history.
        """
        self.load_user_profiles()
        self.translation_history = []

    def get_current_datetime(self):
        """
        Retrieves the current date and time in the computer's local timezone.
        Returns a dictionary with 'datetime' and 'timezone' keys.
        """
        # Get the current date and time in the computer's local timezone
        local_timezone = get_localzone()
        local_time = datetime.datetime.now(local_timezone)
        
        # Get the English code for the timezone
        timezone_code = local_timezone.tzname(local_time)

        return {"datetime": local_time.isoformat(), "timezone": timezone_code}

    def load_user_profiles(self):
        """
        Loads user profiles from the 'user_profiles.json' file.
        If the file does not exist or is empty, initializes an empty user profiles dictionary.
        """
        try:
            with open("user_profiles.json", "r") as file:
                data = file.read()
                if data:
                    self.user_profiles = json.loads(data)
                else:
                    self.user_profiles = {}
        except (FileNotFoundError, JSONDecodeError):
            self.user_profiles = {}

    def save_user_profiles(self):
        """
        Saves user profiles to the 'user_profiles.json' file.
        """
        with open("user_profiles.json", "w") as file:
            json.dump(self.user_profiles, file, indent=4)

    def get_user_profile(self, user_id):
        """
        Retrieves the user profile for the given user ID.
        If the user does not have a profile, creates an empty profile with the default target language 'en'.
        Returns the user profile.
        """
        return self.user_profiles.setdefault(user_id, {"target_lang": "en"})

    def save_user_profile(self, user_id, profile):
        """
        Saves the user profile for the given user ID.
        """
        self.user_profiles[user_id] = profile
        self.save_user_profiles()

    def detect_language(self, text):
        """
        Detects the language of the input text using the langdetect library.
        Returns the detected language code.
        """
        try:
            detected_lang = detect(text)
            return detected_lang
        except Exception as e:
            raise RuntimeError(f"Error detecting language: {str(e)}")
    
    def load_translation_history(self):
        """
        Loads translation history from the 'translation_history.json' file.
        If the file does not exist or is empty, initializes an empty translation history list.
        """
        try:
            with open("translation_history.json", "r") as file:
                data = file.read()
                if data:
                    self.translation_history = json.loads(data)
                else:
                    self.translation_history = []
        except (FileNotFoundError, JSONDecodeError):
            self.translation_history = []

    def save_translation_history(self):
        """
        Saves translation history to the 'translation_history.json' file.
        """
        with open("translation_history.json", "w") as file:
            json.dump(self.translation_history, file, indent=4)

    def append_to_translation_history(self, entry):
        """
        Appends an entry to the translation history.
        Loads the existing history, appends the new entry, and saves the updated history.
        """
        self.load_translation_history()  # Load existing history
        self.translation_history.append(entry)
        self.save_translation_history()  # Save the updated history

    def translate(self, text, user_id):
        """
        Translates the given text based on the user's profile target language.
        Appends the translation to the translation history.
        Returns the translated text.
        """
        user_profile = self.get_user_profile(user_id)
        target_lang = user_profile["target_lang"]
        source_lang = self.detect_language(text)
        model_name = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"
        try:
            model = MarianMTModel.from_pretrained(model_name)
            tokenizer = MarianTokenizer.from_pretrained(model_name)

            input_ids = tokenizer.encode(text, return_tensors="pt")
            output_ids = model.generate(input_ids, max_length=50, num_beams=5)
            translated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

            entry = {
                "user_id": user_id, 
                "timestamp": self.get_current_datetime(), 
                "input_text": text, 
                "translated_text": translated_text}
            self.append_to_translation_history(entry)  # Append to history

            return translated_text
        except RuntimeError as re:
            raise re
        except Exception as e:
            raise RuntimeError(f"Error during translation: {str(e)}")

    def register_user(self):
        """
        Registers a new user by taking user ID and target language as input.
        Creates an empty profile for the new user and saves it.
        """
        user_id = input("Enter your new user ID: ")
        target_lang = input("Enter your target language code (e.g., en): ")
        
        profile = {"target_lang": target_lang}
        self.get_user_profile(user_id)  # Create an empty profile for the new user
        self.save_user_profile(user_id, profile)
        
        print(f"User '{user_id}' registered successfully with target language '{target_lang}'!")

    def chat(self, user_id):
        """
        Initiates a chat session with the user.
        Allows the user to input text, translates it, and prints the translated text.
        Ends the conversation if the user types 'exit'.
        """
        print("Welcome to the Conversational Translator!")
        print("Type 'exit' to end the conversation.")

        while True:
            user_input = input("You: ")

            if user_input.lower() == 'exit':
                print("Goodbye!")
                break

            try:
                translated_text = self.translate(user_input, user_id)
                print(f"Translated Text: {translated_text}")
            except RuntimeError as re:
                print(f"Error: {re}")

if __name__ == "__main__":
    translator = ConversationTranslator()

    while True:
        user_option = input("Do you have a user ID? (yes/no): ").lower()

        if user_option == 'yes':
            user_id = input("Enter your user ID: ")
            break
        elif user_option == 'no':
            translator.register_user()
            user_id = input("Enter your newly created user ID: ")
            break
        else:
            print("Invalid option. Please enter 'yes' or 'no'.")

    try:
        translator.chat(user_id)
    except RuntimeError as re:
        print(f"Error initializing translator: {re}")