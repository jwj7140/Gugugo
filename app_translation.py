import gradio as grad
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, StoppingCriteria, StoppingCriteriaList

model_id = "squarelike/Gugugo-koen-7B-V1.1-GPTQ"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map={"":0})

model.eval()
model.config.use_cache = True  # silence the warnings. Please re-enable for inference!


class StoppingCriteriaSub(StoppingCriteria):

    def __init__(self, stops = [], encounters=1):
        super().__init__()
        self.stops = [stop for stop in stops]

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor):
        for stop in self.stops:
            if torch.all((stop == input_ids[0][-len(stop):])).item():
                return True

        return False

stop_words_ids = torch.tensor([[829, 45107, 29958], [1533, 45107, 29958], [829, 45107, 29958], [21106, 45107, 29958]]).to("cuda")
stopping_criteria = StoppingCriteriaList([StoppingCriteriaSub(stops=stop_words_ids)])


def gen(lan="en", x=""):
    if (lan == "ko"):
        start = "### 영어:"
        prompt = f"### 한국어: {x}</끝>\n### 영어:"
    else:
        start = "### 한국어:"
        prompt = f"### 영어: {x}</끝>\n### 한국어:"
    gened = model.generate(
        **tokenizer(
            prompt,
            return_tensors='pt',
            return_token_type_ids=False
        ).to("cuda"),
        max_new_tokens=2048,
        temperature=0.3,
        num_beams=5,
        stopping_criteria=stopping_criteria
    )
    text = tokenizer.decode(gened[0][1:])
    text = text[text.find(start)+len(start)+1:]
    return text[:text.find("</끝>")]



def translate(text_to_translate, tr_type):
    response = ""
    if (tr_type == "EN->KO"):
        response = gen(lan="en", x=text_to_translate)
        print({"type":"enko", "input":text_to_translate, "output":response})
    elif (tr_type == "KO->EN"):
        response = gen(lan="ko", x=text_to_translate)
        print({"type":"koen", "input":text_to_translate, "output":response})
    return response



grad.Interface(translate, inputs=["text", grad.Radio(["EN->KO", "KO->EN"], label="language")], outputs=["text"], title="Gugugo-koen-7B-v1.1").launch(share=True)