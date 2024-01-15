from transformers import MarianMTModel, MarianTokenizer

class ConversationTranslator:
    def __init__(self, model_name="Helsinki-NLP/opus-mt-fr-en"):
        self.model = MarianMTModel.from_pretrained(model_name)
        self.tokenizer = MarianTokenizer.from_pretrained(model_name)

    def translate(self, text):
        input_ids = self.tokenizer.encode(text, return_tensors="pt")
        output_ids = self.model.generate(input_ids, max_length=50, num_beams=5)
        translated_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return translated_text

    def chat(self):
        print("Welcome to the Conversational Translator!")
        print("Type 'exit' to end the conversation.")

        while True:
            user_input = input("You: ")

            if user_input.lower() == 'exit':
                print("Goodbye!")
                break

            translated_text = self.translate(user_input)
            print(f"Translated Text: {translated_text}")

if __name__ == "__main__":
    translator = ConversationTranslator()
    translator.chat()