<p align="center" width="100%">
<img src="assets/logo.png" alt="Gugugo logo" style="width: 300px; height:300px; display: block; margin: auto; border-radius: 50%;">
</p>

## Update Logs
- 2023.07.18: [🤗Gugugo-koen-1.3B-V0.95](https://huggingface.co/squarelike/Gugugo-koen-1.3B-V0.95)를 공개합니다.(LoRA로 학습, 병합모델)
- 2023.07.13: [Gugugo-koen-1.3B-V0.9 학습 코드](https://github.com/jwj7140/Gugugo/blob/main/GugugoTrain.ipynb)를 공개합니다.
- 2023.07.13: Polyglot-ko 1.3B를 기반으로 [AIHUB](https://aihub.or.kr/) 970만 데이터가 학습된 [🤗Gugugo-koen-1.3B-V0.9](https://huggingface.co/squarelike/Gugugo-koen-1.3B-V0.9)를 공개합니다.(LoRA로 학습, 병합모델)


# Gugugo: Korean translation model based on Polyglot-ko

[Polyglot-ko](https://huggingface.co/EleutherAI/polyglot-ko-1.3b)를 기반으로 만들어진 한국어 번역 모델입니다.

## Gugugo-koen-1.3B-V0.9 ~ V0.95

### 데이터셋

[AIHUB "기술과학 분야 한-영 번역 병렬 말뭉치 데이터"](https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=71266)

[AIHUB "일상생활 및 구어체 한-영 번역 병렬 말뭉치 데이터"](https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=71265)

[AIHUB "전문분야 영-한·중-한 번역 말뭉치 (식품)"](https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=71262)

[AIHUB "한국어-영어 번역 말뭉치(기술과학)"](https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=124)

[AIHUB "한국어-영어 번역 말뭉치(사회과학)"](https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=125)

[AIHUB "한국어-영어 번역(병렬) 말뭉치"](https://aihub.or.kr/aihubdata/data/view.do?dataSetSn=126)


한국어-영어 전체 약 970만 문장의 데이터를 사용했습니다.

### 프롬프트

- 한국어 -> 영어
```
### 영어: hello?</끝>
### 한국어:
```

- 영어 -> 한국어
```
### 한국어: 안녕하세요?</끝>
### 영어:
```

### 학습

#### V0.9

QLoRA를 사용해 RTX4090 24GB 1대로 학습을 진행했습니다.
- Epoch: 1
- learning-rate: 3e-4
- batch_size: 16
- Lora r: 8
- Lora target modules: query_key_value

![Train Loss Graph](./assets/Gugugo-koen-1.3B-V0.9_loss.png)
![Learning Rate Graph](./assets/Gugugo-koen-1.3B-V0.9_learning_rate.png)

#### V0.95

Gugugo-koen-1.3B-V0.9를 기반으로 같은 데이터셋을 1Epoch 더 학습시켰습니다.

QLoRA를 사용해 RTX4090 24GB 1대로 학습을 진행했습니다.
- Epoch: 1
- learning-rate: 3e-4
- batch_size: 16
- Lora r: 8
- Lora target modules: query_key_value

![Train Loss Graph](./assets/Gugugo-koen-1.3B-V0.95_loss.png)



### 출력 예시(V0.95)

```
### 영어: hello?</끝>
### 한국어: 안녕하세요?</끝>
```
```
### 영어: You’re misunderstanding right now. Hear me out.</끝>
### 한국어(v0.9): 지금 이해가 안 되는 거야. 내 말 들어.</끝>
### 한국어(v0.95): 지금 오해하신 거예요, 제 말 잘 들으세요.</끝>
```
```
### 영어: All you need in this life is ignorance and confidence, then success is sure.</끝>
### 한국어(v0.9): 이 세상에는 당신이 알고 있는 것만으로는 부족하고, 자신감이 있어야 성공할 수 있다.</끝>
### 한국어(v0.95): 이 인생에서 필요한 것은 모두 무지와 자신감이며, 성공은 확실하다.</끝>
```
```
### 영어: If you are not willing to risk the usual, you will have to settle for the ordinary.</끝>
### 한국어(v0.9): 평소와 같은 위험을 감수하기 싫다면 평범한 것으로 타협해야 합니다.</끝>
### 한국어(v0.95): 평소에 위험을 감수하지 않으면 평범한 것으로 타협해야 합니다.</끝>
```
```
### 영어: The Federal Aviation Administration has certified for testing a vehicle that a California startup describes as a flying car — the first fully electric vehicle that can both fly and travel on roads to receive US government approval.</끝>
### 한국어(v0.9): 연방항공청은 캘리포니아 스타트업이 미국 정부의 승인을 받기 위해 도로 위를 날아다니고 여행할 수 있는 첫 번째 완전 전기 자동차인 '날아다니는 자동차'로 묘사한 차량을 시험하도록 인증했다.</끝>
### 한국어(v0.95): 연방항공청은 캘리포니아 스타트업이 비행 자동차로 묘사한 차량을 미국 정부 승인을 받기 위해 도로에서 비행하고 여행할 수 있는 첫 번째 완전 전기 자동차로 인증했다.
```
```
### 한국어: 한편 금융위원회와 금융감독원의 '6월 가계대출 동향'에 따르면 은행권과 제2금융권을 포함한 전 금융권 가계대출은 지난달 3조 5천억원 증가해 3개월 연속 증가세를 이어갔다.</끝>
### 영어(v0.9): Meanwhile, according to the Financial Services Commission and the Financial Servic..., the total number of household loans increased by 3.5 trillion won last month, including the banking sector and the secondary financial sector, according to the FSS and the Financial Service of Korea.</끝>
### 영어(v0.95): Meanwhile, according to the Financial Services Commission and the Financial Supervisory Service\'s "Monthly Household Loan Trends" in June, 3.5 trillion won in household loans including the banking sector and the second-largest financial sector increased the number of three months in a year.</끝>
```
```
### 한국어: 미국 경비 보안 업체 ADT에 따르면 남아프리카공화국은 안전 점수 10점 만점에 1점도 채 되지 않는 0.81점을 기록하며 세계에서 가장 위험한 휴양지 1위에 올랐다.</끝>
### 영어(v0.9): According to ADT, a US security security company, South Africa has recorded 0.81 points, as the world's most dangerous resort is ranked as the world's top 10.</끝>
### 영어(v0.95): According to ADT, a US security security company, South Africa ranked the world's most dangerous resort in 0.81 points, with only 1 point in the safety score of 10 points.</끝>
```
```
### 한국어: 나는 무엇인지 그리워 이 많은 별빛이 내린 언덕 위에 내 이름자를 써 보고 흙으로 덮어 버리었습니다.</끝>
### 영어(v0.9): I wanted to remember what it was, and I wrote my name on the hill above the many stars.</끝>
### 영어(v0.95): I want to remember what it is, and I wrote my name on the hill above the many stars, and put it into soil.</끝>
```

### 한계점

Polyglot-ko를 기반으로 하기 때문에 영어->한글 번역에서 더 성능이 좋습니다.

단문 데이터로 학습되었기 때문에 장문 번역에서 낮은 성능을 보입니다.

데이터셋에서 구어체의 비중이 적기 때문에 구어체 번역에서 낮은 성능을 보입니다.

## TO DO LIST

- [sharegpt_deepl_ko 데이터셋](https://huggingface.co/datasets/junelee/sharegpt_deepl_ko)을 활용한 장문 번역 학습
- 관용어 및 비속어 추가 학습 진행
- RLHF 강화학습 진행
