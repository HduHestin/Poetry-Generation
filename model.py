import paddle
from paddlenlp.transformers import BertModel, BertForTokenClassification
from paddle.nn import Layer, Linear, Softmax


class PoetryBertModel(Layer):
    """
    基于BERT预训练模型的诗歌生成模型
    """

    def __init__(self, pretrained_bert_model: str, input_length: int):
        super(PoetryBertModel, self).__init__()
        bert_model = BertModel.from_pretrained(pretrained_bert_model)
        self.vocab_size, self.hidden_size = bert_model.embeddings.word_embeddings.parameters()[0].shape
        self.bert_for_class = BertForTokenClassification(bert_model, self.vocab_size)
        # 生成下三角矩阵，用来mask句子后边的信息
        self.sequence_length = input_length
        # lower_triangle_mask为input_length * input_length的下三角矩阵（包含主对角线），该掩码作为注意力掩码的一部分（在forward的
        # 处理中为0的部分会被处理成无穷小量，以方便在计算注意力权重的时候保证被掩盖的部分权重约等于0）。而之所以写为下三角矩阵的形式，与
        # transformer的多头注意力计算的机制有关，细节可以了解相关论文获悉。
        self.lower_triangle_mask = paddle.tril(paddle.tensor.full((input_length, input_length), 1, 'float32'))

    def forward(self, token, token_type, input_mask, input_length=None):
        # 计算attention mask
        mask_left = paddle.reshape(input_mask, input_mask.shape + [1])
        mask_right = paddle.reshape(input_mask, [input_mask.shape[0], 1, input_mask.shape[1]])
        # 输入句子中有效的位置
        mask_left = paddle.cast(mask_left, 'float32')
        mask_right = paddle.cast(mask_right, 'float32')
        attention_mask = paddle.matmul(mask_left, mask_right)
        # 注意力机制计算中有效的位置
        if input_length is not None:
            # 之所以要再计算一次，是因为用于推理预测时，可能输入的长度不为实例化时设置的长度。这里的模型在训练时假设输入的
            # 长度是被填充成一致的——这一步不是必须的，但是处理成一致长度比较方便处理（对应地，增加了显存的用度）。
            lower_triangle_mask = paddle.tril(paddle.tensor.full((input_length, input_length), 1, 'float32'))
        else:
            lower_triangle_mask = self.lower_triangle_mask
        attention_mask = attention_mask * lower_triangle_mask
        # 无效的位置设为极小值
        attention_mask = (1 - paddle.unsqueeze(attention_mask, axis=[1])) * -1e10
        attention_mask = paddle.cast(attention_mask, self.bert_for_class.parameters()[0].dtype)

        output_logits = self.bert_for_class(token, token_type_ids=token_type, attention_mask=attention_mask)

        return output_logits


class PoetryBertModelLossCriterion(Layer):
    def forward(self, pred_logits, label, input_mask):
        loss = paddle.nn.functional.cross_entropy(pred_logits, label, ignore_index=0, reduction='none')
        masked_loss = paddle.mean(loss * input_mask, axis=0)
        return paddle.sum(masked_loss)


from paddle.static import InputSpec
from paddlenlp.metrics import Perplexity
from paddle.optimizer import AdamW

net = PoetryBertModel('bert-base-chinese', 128)

token_ids = InputSpec((-1, 128), 'int64', 'token')
token_type_ids = InputSpec((-1, 128), 'int64', 'token_type')
input_mask = InputSpec((-1, 128), 'float32', 'input_mask')
label = InputSpec((-1, 128), 'int64', 'label')

inputs = [token_ids, token_type_ids, input_mask]
labels = [label, input_mask]

model = paddle.Model(net, inputs, labels)
model.prepare(optimizer=AdamW(learning_rate=0.0001, parameters=model.parameters()), loss=PoetryBertModelLossCriterion(), metrics=[Perplexity()])
