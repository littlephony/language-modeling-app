import torch
from torch import nn
from torch.distributions import Categorical
import numpy as np


class TextGenerationNet(nn.Module):
    def __init__(self, vocab_size, embed_dim, rnn_hidden_size):
        super().__init__()

        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.rnn_hidden_size = rnn_hidden_size
        self.rnn = nn.LSTM(embed_dim, rnn_hidden_size, batch_first=True)
        self.fc = nn.Linear(rnn_hidden_size, vocab_size)

    def forward(self, x, hidden, cell):
        out = self.embedding(x).unsqueeze(1)
        out, (hidden, cell) = self.rnn(out, (hidden, cell))
        out = self.fc(out).reshape(out.size(0), -1)
        return out, hidden, cell

    def init_hidden(self, batch_size):
        hidden = torch.zeros(1, batch_size, self.rnn_hidden_size)
        cell = torch.zeros(1, batch_size, self.rnn_hidden_size)
        return hidden, cell


class TextGenerationModel:
    def __init__(self):
        self._load_characters()
        self.model = TextGenerationNet(
            vocab_size=len(self._char_array), embed_dim=256, rnn_hidden_size=512
        )
        self.model.load_state_dict(torch.load("../model/model.pt", map_location="cpu"))

    def _load_characters(self):
        with open("../model/input.txt", "r", encoding="utf8") as f:
            chars = sorted(set(" ".join(f.read().split())))

        self._chars_to_int = {char: i for i, char in enumerate(chars)}
        self._char_array = np.array(chars)

    @torch.no_grad()
    def generate(self, input_prompt, generate_len=500):
        encoded_input = torch.tensor([self._chars_to_int[c] for c in input_prompt])
        encoded_input = torch.reshape(encoded_input, (1, -1))
        generated_string = input_prompt

        hidden, cell = self.model.init_hidden(1)
        for c in range(len(input_prompt) - 1):
            _, hidden, cell = self.model(encoded_input[:, c].view(1), hidden, cell)

        last_char = encoded_input[:, -1]
        for i in range(generate_len):
            logits, hidden, cell = self.model(last_char.view(1), hidden, cell)
            logits = torch.squeeze(logits, 0)
            scaled_logits = logits
            m = Categorical(logits=scaled_logits)
            last_char = m.sample()
            generated_string += str(self._char_array[last_char])

        return generated_string
