from abc import ABC, abstractmethod
import logging
from openai import OpenAI
from anthropic import Anthropic
from prompts import personas, prompts

class NullLogger(logging.Logger):
    def __init__(self):
        super().__init__("null_logger")
        self.addHandler(logging.NullHandler())


class AbstractSummarizer(ABC):
    def __init__(self, client, model, cpmm_response, cpmm_prompt, logger=None):
        self.client = client
        self.model = model
        self.cost_per_million_response = cpmm_response
        self.cost_per_million_prompt = cpmm_prompt
        self.temperature = 0
        self.max_tokens = 1024
        self.tokens_answer = 0
        self.tokens_prompt = 0
        self.logger = logger or NullLogger()

        self.persona = None
        self.transcript = None

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def prompt(self, prompt_type: str):
        pass

    def expense(self):
        answer_price = self.tokens_answer * (self.cost_per_million_response / 1e6)
        prompt_price = self.tokens_prompt * (self.cost_per_million_prompt / 1e6)
        total_price = prompt_price + answer_price

        return f"Cost for {self.name} Model {self.model}\n prompt ${prompt_price:.2f}\n answer ${answer_price:.2f} +\n -------------- \n TOTAL  ${total_price:.2f}"

    def system_prompt(self):
        if not self.persona:
            self.persona = 'default'
            
        persona = personas.get(self.persona)
        if not persona:
            raise ValueError(f"Persona Validation Error: '{name}' is not an available system persona")

        return persona

    def user_prompt(self, name):
        unformatted_prompt = prompts.get(name)
        if not unformatted_prompt:
            raise ValueError(f"Prompt Validation Error: '{prompt_type}' is not an available prompt")

        return unformatted_prompt.format(transcription=self.transcript)


class OpenAISummarizer(AbstractSummarizer):
    def __init__(self, model, cpmm_response, cpmm_prompt, logger=None):
        super().__init__(
            client=OpenAI(),
            model=model,
            cpmm_response=cpmm_response,
            cpmm_prompt=cpmm_prompt,
            logger=logger
        )
    
    @property
    def name(self):
        return 'OpenAI'

    def prompt(self, prompt_type: str):        
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=[
                {"role": "system", "content": self.system_prompt()},
                {"role": "user", "content": prompts["example_prompt"]},
                {"role": "assistant", "content": prompts["example_response"]},
                {"role": "user", "content": self.user_prompt(prompt_type)},
            ],
        )
        self.tokens_answer += response.usage.completion_tokens
        self.tokens_prompt += response.usage.prompt_tokens
        self.logger.info(f"{prompt_type} tokens - Our Prompt:{response.usage.prompt_tokens}, AI Response:{response.usage.completion_tokens}")
        return "".join(choice.message.content for choice in response.choices)



class AnthropicSummarizer(AbstractSummarizer):
    def __init__(self, model, cpmm_response, cpmm_prompt, logger=None):
        super().__init__(
            client=Anthropic(),
            model=model,
            cpmm_response=cpmm_response,
            cpmm_prompt=cpmm_prompt,
            logger=logger
        )
    
    @property
    def name(self):
        return 'Anthropic'

    def prompt(self, prompt_type: str):
        message = self.client.messages.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            system=self.system_prompt(),
            messages=[
                {"role": "user", "content": prompts["example_prompt"]},
                {"role": "assistant", "content": prompts["example_response"]},
                {"role": "user", "content": self.user_prompt(prompt_type)},
            ],
        )
        self.tokens_answer += message.usage.output_tokens
        self.tokens_prompt += message.usage.input_tokens
        self.logger.info(f"{prompt_type} tokens - Our Prompt:{message.usage.input_tokens}, AI Response:{message.usage.output_tokens}")
        return "".join(block.text for block in message.content)
        


class SummarizationFactory:
    @staticmethod
    def get_summarizer(ai_type, model, cpmm_response, cpmm_prompt, logger=None):
        if ai_type == "openai":
            return OpenAISummarizer(model, cpmm_response, cpmm_prompt, logger)
        elif ai_type == "anthropic":
            return AnthropicSummarizer(model, cpmm_response, cpmm_prompt, logger)
        else:
            raise ValueError(f"Unknown summarizer type: {ai_type}")
