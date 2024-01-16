# Conversational Translator

A conversational translator that allows users to register, chat, and translate messages. It keeps track of user profiles and translation history.

## Installation

Make sure you have Python installed on your system.

```bash
pip install python
```
## Usage

Run the following command to start the conversational translator:

```bash
python NativeFlow.py
```
Follow the prompts to register or provide your existing user ID. Start chatting and enjoy translations!

## Features

`User Registration`: Choose to register as a new user or provide your existing user ID. New users need to provide a user ID and target language code.

`Translation`: Input text, and the translator will automatically detect the language and translate it based on the user's target language.

`Translation History`: All translations are stored in the translation_history.json file, including user ID, timestamp, input text, and translated text.

`User Profiles`: User profiles are stored in the user_profiles.json file, containing user IDs and their target languages.

## Code Structure
The code is organized into a class-based structure:

`ConversationTranslator`: The main class handling user registration, translation, and conversation.

`get_current_datetime`: Method to retrieve the current date and time with timezone.

`load_user_profiles` and `save_user_profiles`: Methods to load and save user profiles.

`get_user_profile` and `save_user_profile`: Methods to retrieve and save user profiles.

`detect_language`: Method to detect the language of input text using the langdetect library.

`load_translation_history` and `save_translation_history`: Methods to load and save translation history.

`append_to_translation_history`: Method to append an entry to the translation history.

`translate`: Method to translate input text based on the user's profile.

`register_user`: Method to register a new user.

`chat`: Method to initiate a chat session with the user.

## Dependencies
`transformers`: Library for Natural Language Processing tasks.

`langdetect`: Library for language detection.


