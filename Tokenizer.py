#pragma once
#include <map>
#include <vector>
#include <string>
#include <fstream>
#include <iostream>

class TokenizerBase:
    def __init__(self):
        self.tokenizer_token2idx = {}

    def load_tokenize(self, vocab_path):
        raise NotImplementedError("Subclasses should implement this!")

    def encode_text(self, text,):
        raise NotImplementedError("Subclasses should implement this!")
    
class TokenizerClip(TokenizerBase):
    def __init__(self):
        super().__init__()

    def stringSplit(self, s, delimiter):
        return s.split(delimiter)

    def tokenize(self, token):
        idx = []
        idx.append(49406)
        tokens = self.stringSplit(token, ' ')
        for t in tokens:
            idx.append(self.tokenizer_token2idx[t + "</w>"])
        idx.append(49407)
        return idx

    def load_tokenize(self, vocab_path):
        with open(vocab_path, 'r') as f:
            for idx, line in enumerate(f):
                self.tokenizer_token2idx[line.strip()] = idx
        return True

    def encode_text(self, text, pad=77):
        idx = self.tokenize(text)
        if len(idx) < pad:
            idx.extend([0] * (pad - len(idx)))
        return idx
    
if __name__ == "__main__":
    tokenizer = TokenizerClip()
    tokenizer.load_tokenize("vocab.txt")
    print(tokenizer.encode_text("hello world"))