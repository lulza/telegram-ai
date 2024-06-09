from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from typing import Final

# available models
blenderbot: Final = "facebook/blenderbot-400M-distill"
mGPT: Final = "ai-forever/mGPT"

# model types
conversational: Final = "conversational"
text_generation: Final = "text-generation"

models_welcome_messages = {
    blenderbot: "Hello! I'm blenderbot, my full name is `facebook/blenderbot-400M-distill`. I would be glad to discuss something with you!",
    mGPT: "Привет! Меня зовут mGPT или же `ai-forever/mGPT`. Я буду рад пообщаться на любую тему!"
}

class Model:
    """
    Model can load any model that you want from hugging face but for different models
        you may need to configure discuss function, change pipeline task or just rewrite it a bit))
    """
    available_models = {
        blenderbot: conversational,
        mGPT: text_generation,
    }


    def __init__(self, model_name=blenderbot):
        self.load_model(model_name)
        

    def load_model(self, model_name) -> str:
        if model_name not in self.available_models.keys():
            raise Exception("Model is not available")
        
        self.model_name = model_name
        self.model_type = self.available_models[model_name]
        
        if self.model_type == conversational:
            self.chatbot = pipeline(model=model_name)
        elif self.model_type == text_generation:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
        else:
            raise Exception("Model type is unknown")
    
    def get_welcome_message(self):
        try:
            return models_welcome_messages[self.model_name]
        except KeyError:
            raise Exception("model name is unknown or doesn't have a welcome message")

    
    def discuss(self, prompt: str) -> str:
        if self.model_type == conversational:
            return self.respond(prompt)
        elif self.model_type == text_generation:
            return self.generate_text(prompt)
        

    def respond(self, prompt: str) -> str:
        conversation = self.chatbot(prompt)
        result = conversation[-1]["generated_text"]
        
        return result
    

    def generate_text(self, prompt: str) -> str:
        text = f"Вопрос: {prompt}\nОтвет:"
        input_ids = self.tokenizer.encode(text, return_tensors="pt")

        out = self.model.generate(input_ids, do_sample=False, max_length=100)
        generated_text = list(map(self.tokenizer.decode, out))[0]
        result = generated_text.split("Ответ:")[-1].split("\n")[0].strip()

        return result
