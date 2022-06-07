import re
import emoji

from sklearn.preprocessing import MultiLabelBinarizer
from soynlp.normalizer import repeat_normalize
import transformers

mlb = MultiLabelBinarizer()
mlb.fit([[i for i in range(44)]])

emojis = ''.join(emoji.UNICODE_EMOJI.keys())
pattern = re.compile(f'[^ .,?!/@$%~％·∼()\x00-\x7Fㄱ-ㅣ가-힣{emojis}]+')
url_pattern = re.compile(
    r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')

def clean(x):
    x = pattern.sub(' ', x)
    x = url_pattern.sub('', x)
    x = x.strip()
    x = repeat_normalize(x, num_repeats=2)
    return x

def do_inference(text: str, threshold: float, pipe: transformers.pipelines.text_classification.TextClassificationPipeline):
    if not 0 <= threshold <=1:
        raise ValueError("theshold must be a float b/w 0 ~ 1.")
    results = {}
    cur_result = {}
    
    text = clean(text)
    out = pipe(text, stride=128, return_overflowing_tokens=True, padding=True, truncation=True)[0]
    for feeling in out:
        if feeling["score"] > threshold:
            cur_result[feeling["label"]] = round(feeling["score"], 2)
    cur_result = sorted(cur_result.items(), key=lambda x: x[1], reverse=True)
    results = cur_result[:10]
    
    return results