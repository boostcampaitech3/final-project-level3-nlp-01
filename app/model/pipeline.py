import numpy as np
from typing import Dict

from transformers.models.auto.modeling_auto import MODEL_FOR_SEQUENCE_CLASSIFICATION_MAPPING
from transformers.pipelines.base import GenericTensor
from transformers.pipelines.text_classification import sigmoid, softmax, ClassificationFunction, TextClassificationPipeline

class SongPipeline(TextClassificationPipeline):

    def preprocess(self, inputs, **tokenizer_kwargs) -> Dict[str, GenericTensor]:
        return_tensors = self.framework
        tokenized_result = self.tokenizer(inputs, return_tensors=return_tensors, **tokenizer_kwargs)
        tokenized_result.pop('overflow_to_sample_mapping')
        return tokenized_result

    def postprocess(self, model_outputs, function_to_apply=None, return_all_scores=False):
        # Default value before `set_parameters`
        if function_to_apply is None:
            if self.model.config.problem_type == "multi_label_classification" or self.model.config.num_labels == 1:
                function_to_apply = ClassificationFunction.SIGMOID
            elif self.model.config.problem_type == "single_label_classification" or self.model.config.num_labels > 1:
                function_to_apply = ClassificationFunction.SOFTMAX
            elif hasattr(self.model.config, "function_to_apply") and function_to_apply is None:
                function_to_apply = self.model.config.function_to_apply
            else:
                function_to_apply = ClassificationFunction.NONE

        outputs = model_outputs["logits"]
        outputs = outputs.numpy()

        if function_to_apply == ClassificationFunction.SIGMOID:
            scores = sigmoid(outputs)
        elif function_to_apply == ClassificationFunction.SOFTMAX:
            scores = softmax(outputs)
        elif function_to_apply == ClassificationFunction.NONE:
            scores = outputs
        else:
            raise ValueError(f"Unrecognized `function_to_apply` argument: {function_to_apply}")
        
        scores = np.mean(scores, axis=0)
        
        if return_all_scores:
            return [{"label": self.model.config.id2label[i], "score": score.item()} for i, score in enumerate(scores)]
        else:
            return {"label": self.model.config.id2label[scores.argmax().item()], "score": scores.max().item()}
