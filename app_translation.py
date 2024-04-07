import gradio as grad
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, StoppingCriteria, StoppingCriteriaList, BitsAndBytesConfig
import argparse

parser = argparse.ArgumentParser(description='WebUI for Gugugo')

parser.add_argument('--type', type=str, default='koja', help='translation type. "koen" or "koja" (default: koen)')
config = parser.parse_args()


class StoppingCriteriaSub(StoppingCriteria):

    def __init__(self, stops = [], encounters=1):
        super().__init__()
        self.stops = [stop for stop in stops]

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor):
        for stop in self.stops:
            if torch.all((stop == input_ids[0][-len(stop):])).item():
                return True

        return False



if (config.type == "koen"):
    model_id = "squarelike/Gugugo-koen-7B-V1.1-GPTQ"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, device_map={"":0})
    stop_words_ids = torch.tensor([[829, 45107, 29958], [1533, 45107, 29958], [829, 45107, 29958], [21106, 45107, 29958]]).to("cuda")
    stopping_criteria = StoppingCriteriaList([StoppingCriteriaSub(stops=stop_words_ids)])
elif (config.type == "koja"):
    model_id = "squarelike/Gugugo-koja-1.3B-V0.95"
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config, device_map={"":0})
    stop_words_ids = torch.tensor([[31, 18, 5568, 33], [422, 18, 5568, 33]]).to("cuda")
    stopping_criteria = StoppingCriteriaList([StoppingCriteriaSub(stops=stop_words_ids)])

model.eval()
model.config.use_cache = True  # silence the warnings. Please re-enable for inference!



def gen_koen(lan="en", x=""):
    if (lan == "ko"):
        prompt = f"### 한국어: {x}</끝>\n### 영어:"
    else:
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
    text = tokenizer.batch_decode(gened[:, len(tokenizer.encode(prompt)):])[0]
    return text[:text.find("</끝>")]


def translate_koen(text_to_translate, tr_type):
    response = ""
    if (tr_type == "EN->KO"):
        response = gen_koen(lan="en", x=text_to_translate)
        print({"type":"enko", "input":text_to_translate, "output":response})
    elif (tr_type == "KO->EN"):
        response = gen_koen(lan="ko", x=text_to_translate)
        print({"type":"koen", "input":text_to_translate, "output":response})
    return response

def gen_koja(lan="ja", x=""):
    if (lan == "ko"):
        prompt = f"### 한국어: {x}</끝>\n### 일본어:"
    else:
        prompt = f"### 일본어: {x}</끝>\n### 한국어:"
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
    text = tokenizer.batch_decode(gened[:, len(tokenizer.encode(prompt)):])[0]
    return text[:text.find("</끝>")]

def translate_koja(text_to_translate, tr_type):
    response = ""
    if (tr_type == "JA->KO"):
        response = gen_koja(lan="ja", x=text_to_translate)
        print({"type":"jako", "input":text_to_translate, "output":response})
    elif (tr_type == "KO->JA"):
        response = gen_koja(lan="ko", x=text_to_translate)
        print({"type":"koja", "input":text_to_translate, "output":response})
    return response


if (config.type == "koen"):
    grad.Interface(translate_koen, inputs=["text", grad.Radio(["EN->KO", "KO->EN"], label="language")], outputs=["text"], title="Gugugo-koen-7B-v1.1").launch(share=True)
elif (config.type == "koja"):
    grad.Interface(translate_koja, inputs=["text", grad.Radio(["JA->KO", "KO->JA"], label="language")], outputs=["text"], title="Gugugo-koja-1.3B-V0.95").launch(share=True)