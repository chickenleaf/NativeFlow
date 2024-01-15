from transformers import MarianMTModel, MarianTokenizer
from langdetect import detect

class ConversationTranslator:
    def __init__(self, target_lang=None):
        self.target_lang = target_lang or "en"

    def detect_language(self, text):
        try:
            detected_lang = detect(text)
            return detected_lang
        except Exception as e:
            raise RuntimeError(f"Error detecting language: {str(e)}")

    def translate(self, text):
        try:
            source_lang = self.detect_language(text)
            self.model_name = f"Helsinki-NLP/opus-mt-{source_lang}-{self.target_lang}"
            self.model = MarianMTModel.from_pretrained(self.model_name)
            self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)

            input_ids = self.tokenizer.encode(text, return_tensors="pt")
            output_ids = self.model.generate(input_ids, max_length=50, num_beams=5)
            translated_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
            return translated_text
        except RuntimeError as re:
            raise re
        except Exception as e:
            raise RuntimeError(f"Error during translation: {str(e)}")

    def chat(self):
        print("Welcome to the Conversational Translator!")
        print("Type 'exit' to end the conversation.")

        while True:
            user_input = input("You: ")

            if user_input.lower() == 'exit':
                print("Goodbye!")
                break

            try:
                translated_text = self.translate(user_input)
                print(f"Translated Text: {translated_text}")
            except RuntimeError as re:
                print(f"Error: {re}")

if __name__ == "__main__":
    target_lang = input("Enter target language code (e.g., en): ")

    try:
        translator = ConversationTranslator(target_lang=target_lang)
        translator.chat()
    except RuntimeError as re:
        print(f"Error initializing translator: {re}")

