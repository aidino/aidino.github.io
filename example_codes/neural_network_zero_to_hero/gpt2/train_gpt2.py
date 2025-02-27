from dataclasses import dataclass
import torch
import torch.nn as nn 
from torch.nn import functional as F

# ------------------------------------------------------------

class CausalSelfAttention(nn.Module):

    def __init__(self, config):
        super().__init__()
        assert config.n_embd % config.n_head == 0
        # key, query, value projections for all heads, but in a batch
        self.c_attn = nn.Linear(config.n_embd, 3 * config.n_embd)
        # output projection
        self.c_proj = nn.Linear(config.n_embd, config.n_embd)
        self.c_proj.NANOGPT_SCALE_INIT = 1
        # regularization
        self.n_head = config.n_head
        self.n_embd = config.n_embd

    def forward(self, x):
        B, T, C = x.size() # batch size, sequence length, embedding dimensionality (n_embd)
        # calculate query, key, values for all heads in batch and move head forward to be the batch dim
        # nh is "number of heads", hs is "head size", and C (number of channels) = nh * hs
        # e.g. in GPT-2 (124M), n_head=12, hs=64, so nh*hs=C=768 channels in the Transformer
        
        # Mỗi head sẽ phụ trách một phần của embedding, do đó cần có yêu cầu n_embd % n_head == 0
        # Giả sử, n_embd = 8 (mỗi token sẽ được đại diện bằng 1 vector có độ dài là 8)
        # Nếu có 2 head, thì mỗi head sẽ xử lý 1 nửa n_embd (vector có độ dài 4) 
        
        qkv = self.c_attn(x) # (B, T, 3*n_embd)
        
         # Split chiều cuối cùng, mỗi phần có độ dài n_embd => tách làm 3 cho 3 vector q, k, v
        q, k, v = qkv.split(self.n_embd, dim=2) # (B, T, n_embd)
        
        # k.view(B, T, self.n_head, C // self.n_head) = (B, T, n_head, hs)
        # hs = head_size : 1 phần của n_embd do head đó phụ trách
        # .transpose(1, 2) : (b, nh, T, hs)
        k = k.view(B, T, self.n_head, C // self.n_head).transpose(1, 2) # (B, nh, T, hs)
        q = q.view(B, T, self.n_head, C // self.n_head).transpose(1, 2) # (B, nh, T, hs)
        v = v.view(B, T, self.n_head, C // self.n_head).transpose(1, 2) # (B, nh, T, hs)
        # Cơ chế này tính toán sự tương tác giữa các vector query (q), key (k), và value (v) 
        # để tạo ra đầu ra dựa trên mức độ "chú ý" giữa chúng.
        # Công thức: Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) * V
        # is_causal: Nếu True, áp dụng causal mask
        # nghĩa là chỉ cho phép chú ý đến các vị trí trước đó trong chuỗi 
        # Transformer Decoder: Với is_causal=True để xử lý tự hồi quy.
        # Transformer Encoder: Với is_causal=False khi tất cả token đều có thể chú ý lẫn nhau.
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True) # flash attention # (B, nh, T, hs)
        
        # contiguous(): Đảm bảo tensor liền kề trong bộ nhớ.
        y = y.transpose(1, 2).contiguous().view(B, T, C) # re-assemble all head outputs side by side
        # output projection
        y = self.c_proj(y)
        return y

class MLP(nn.Module):

    def __init__(self, config):
        super().__init__()
        self.c_fc    = nn.Linear(config.n_embd, 4 * config.n_embd)
        self.gelu    = nn.GELU(approximate='tanh')
        self.c_proj  = nn.Linear(4 * config.n_embd, config.n_embd)
        self.c_proj.NANOGPT_SCALE_INIT = 1

    def forward(self, x):
        x = self.c_fc(x)
        x = self.gelu(x)
        x = self.c_proj(x)
        return x

class Block(nn.Module):

    def __init__(self, config):
        super().__init__()
        self.ln_1 = nn.LayerNorm(config.n_embd)
        self.attn = CausalSelfAttention(config)
        self.ln_2 = nn.LayerNorm(config.n_embd)
        self.mlp = MLP(config)

    def forward(self, x):
        x = x + self.attn(self.ln_1(x))
        x = x + self.mlp(self.ln_2(x))
        return x

@dataclass
class GPTConfig:
    block_size: int = 1024 # max sequence length
    vocab_size: int = 50257 # number of tokens: 50,000 BPE merges + 256 bytes tokens + 1 <|endoftext|> token
    n_layer: int = 12 # number of layers
    n_head: int = 12 # number of heads
    n_embd: int = 768 # embedding dimension

class GPT(nn.Module):

    def __init__(self, config):
        super().__init__()
        self.config = config

        self.transformer = nn.ModuleDict(dict(
            wte = nn.Embedding(config.vocab_size, config.n_embd), # text embedding
            wpe = nn.Embedding(config.block_size, config.n_embd), # position embedding
            h = nn.ModuleList([Block(config) for _ in range(config.n_layer)]), # hidden layer # (B, T, n_embd)
            ln_f = nn.LayerNorm(config.n_embd),
        ))
        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)

        # weight sharing scheme
        self.transformer.wte.weight = self.lm_head.weight

        # init params
        self.apply(self._init_weights)

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            std = 0.02
            if hasattr(module, 'NANOGPT_SCALE_INIT'):
                std *= (2 * self.config.n_layer) ** -0.5
            torch.nn.init.normal_(module.weight, mean=0.0, std=std)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, idx, targets=None):
        # idx is of shape (B, T)
        B, T = idx.size()
        assert T <= self.config.block_size, f"Cannot forward sequence of length {T}, block size is only {self.config.block_size}"
        # forward the token and posisition embeddings
        pos = torch.arange(0, T, dtype=torch.long, device=idx.device) # shape (T)
        pos_emb = self.transformer.wpe(pos) # position embeddings of shape (T, n_embd)
        tok_emb = self.transformer.wte(idx) # token embeddings of shape (B, T, n_embd)
        x = tok_emb + pos_emb
        # forward the blocks of the transformer
        for block in self.transformer.h:
            x = block(x)
        # forward the final layernorm and the classifier
        x = self.transformer.ln_f(x)
        logits = self.lm_head(x) # (B, T, vocab_size)
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1))
        return logits, loss

    @classmethod
    def from_pretrained(cls, model_type):
        """Loads pretrained GPT-2 model weights from huggingface"""
        assert model_type in {'gpt2', 'gpt2-medium', 'gpt2-large', 'gpt2-xl'}
        from transformers import GPT2LMHeadModel
        print("loading weights from pretrained gpt: %s" % model_type)

        # n_layer, n_head and n_embd are determined from model_type
        config_args = {
            'gpt2':         dict(n_layer=12, n_head=12, n_embd=768),  # 124M params
            'gpt2-medium':  dict(n_layer=24, n_head=16, n_embd=1024), # 350M params
            'gpt2-large':   dict(n_layer=36, n_head=20, n_embd=1280), # 774M params
            'gpt2-xl':      dict(n_layer=48, n_head=25, n_embd=1600), # 1558M params
        }[model_type]
        config_args['vocab_size'] = 50257 # always 50257 for GPT model checkpoints
        config_args['block_size'] = 1024 # always 1024 for GPT model checkpoints
        # create a from-scratch initialized minGPT model
        config = GPTConfig(**config_args)
        model = GPT(config)
        
        #Trả về một từ điển chứa tất cả các tham số (weights) và buffer của mô hình minGPT. sd là state_dict này.
        sd = model.state_dict()
        sd_keys = sd.keys()
        # .attn.bias thường là các buffer (ví dụ: mask trong attention), 
        # không phải là tham số có thể học được, nên chúng bị loại bỏ khỏi danh sách sd_keys.
        sd_keys = [k for k in sd_keys if not k.endswith('.attn.bias')] # discard this mask / buffer, not a param

        # Tải một mô hình GPT-2 đã được huấn luyện trước từ thư viện Hugging Face Transformers
        model_hf = GPT2LMHeadModel.from_pretrained(model_type)
        sd_hf = model_hf.state_dict() # sd = state dict, hf: hugging face

        # copy while ensuring all of the parameters are aligned and match in names and shapes
        sd_keys_hf = sd_hf.keys()
        sd_keys_hf = [k for k in sd_keys_hf if not k.endswith('.attn.masked_bias')] # ignore these, just a buffer
        sd_keys_hf = [k for k in sd_keys_hf if not k.endswith('.attn.bias')] # same, just the mask (buffer)
        
        # Đây là danh sách các tên tham số (weights) cần được chuyển vị (transpose) khi sao chép từ mô hình Hugging Face sang GPT.
        transposed = ['attn.c_attn.weight', 'attn.c_proj.weight', 'mlp.c_fc.weight', 'mlp.c_proj.weight']
        # Trong checkpoint của OpenAI (dùng trong Hugging Face), các tầng như Conv1D được sử dụng thay vì Linear. 
        # Khi chuyển sang triển khai minGPT (dùng Linear), các trọng số này cần được chuyển vị để khớp với định dạng.
        
        # attn.c_attn.weight: Trọng số của query/key/value trong attention.
        # mlp.c_fc.weight: Trọng số của fully connected layer đầu tiên trong MLP.
        # attn.c_proj.weight: Trọng số của projection sau attention.
        # mlp.c_proj.weight: Trọng số của fully connected layer thứ hai trong MLP.
        
        assert len(sd_keys_hf) == len(sd_keys), f"mismatched keys: {len(sd_keys_hf)} != {len(sd_keys)}"
        for k in sd_keys_hf:
            if any(k.endswith(w) for w in transposed):
                # Đảm bảo rằng kích thước của trọng số trong Hugging Face (sau khi đảo ngược) khớp với kích thước trong minGPT.
                assert sd_hf[k].shape[::-1] == sd[k].shape
                with torch.no_grad():
                    sd[k].copy_(sd_hf[k].t()) # Chuyển vị trọng số từ Hugging Face (dùng .t() trong PyTorch).
            else:
                # Đảm bảo kích thước của trọng số trong hai mô hình khớp nhau.
                assert sd_hf[k].shape == sd[k].shape
                with torch.no_grad():
                    sd[k].copy_(sd_hf[k])

        return model


    # def configure_optimizers(self, weight_decay, learning_rate, device_type):
    #     # start with all of the candidate parameters (that require grad)
    #     param_dict = {pn: p for pn, p in self.named_parameters()}
    #     param_dict = {pn: p for pn, p in param_dict.items() if p.requires_grad}
    #     # create optim groups. Any parameters that is 2D will be weight decayed, otherwise no.
    #     # i.e. all weight tensors in matmuls + embeddings decay, all biases and layernorms don't.
    #     decay_params = [p for n, p in param_dict.items() if p.dim() >= 2]
    #     nodecay_params = [p for n, p in param_dict.items() if p.dim() < 2]
    #     optim_groups = [
    #         {'params': decay_params, 'weight_decay': weight_decay},
    #         {'params': nodecay_params, 'weight_decay': 0.0}
    #     ]
    #     num_decay_params = sum(p.numel() for p in decay_params)
    #     num_nodecay_params = sum(p.numel() for p in nodecay_params)
    #     if master_process:
    #         print(f"num decayed parameter tensors: {len(decay_params)}, with {num_decay_params:,} parameters")
    #         print(f"num non-decayed parameter tensors: {len(nodecay_params)}, with {num_nodecay_params:,} parameters")
    #     # Create AdamW optimizer and use the fused version if it is available
    #     fused_available = 'fused' in inspect.signature(torch.optim.AdamW).parameters
    #     use_fused = fused_available and device_type == "cuda"
    #     if master_process:
    #         print(f"using fused AdamW: {use_fused}")
    #     optimizer = torch.optim.AdamW(optim_groups, lr=learning_rate, betas=(0.9, 0.95), eps=1e-8, fused=use_fused)
    #     return optimizer

# -----------------------------------------------------------------------------
        

num_return_sequences = 5
max_length = 30

model = GPT.from_pretrained('gpt2')
model.eval()
# model.to('cuda')

# prefix token
import tiktoken

enc = tiktoken.get_encoding('gpt2')
tokens = enc.encode("Hello, I'm a language model,")
tokens = torch.tensor(tokens, dtype=torch.long)
tokens = tokens.unsqueeze(0).repeat(num_return_sequences, 1)
# x = tokens.to('cuda')
x = tokens

torch.manual_seed(42)
# torch.cuda.manual_seed(42)
# generate!
while x.size(1) < max_length: # max_length=30
    # forward the model to get the logits
    with torch.no_grad():
        # Mô hình trả về một tuple, trong đó phần tử đầu tiên là logits với kích thước (B, T, vocab_size)
        logits = model(x)[0] # (B, T, vocab_size)
        # take the logits at the last position
        logits = logits[:, -1, :] # (B, vocab_size)
        # get the probabilities
        probs = F.softmax(logits, dim=-1)
        # do top-k sampling of 50 (huggingface pipeline default)
        # topk_probs here becomes (5, 50), topk_indices is (5, 50)
        topk_probs, topk_indices = torch.topk(probs, 50, dim=-1)
        # select a token from the top-k probabilities
        # note: multinomial does not demand the input to sum to 1
        ix = torch.multinomial(topk_probs, 1) # (B, 1)
        # gather the corresponding indices
        xcol = torch.gather(topk_indices, -1, ix) # (B, 1)
        # append to the sequence
        x = torch.cat((x, xcol), dim=1)

for i in range(num_return_sequences):
    tokens = x[i, :30].tolist()
    decoded = enc.decode(tokens)
    print(">", decoded)