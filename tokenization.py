import  tiktoken 

encoder = tiktoken.encoding_for_model('gpt-4o')

print("Vocab Size", encoder.n_vocab)

text= "Hello, how are you?"
tokens = encoder.encode(text)
print("Tokens", tokens)

my_token = encoder.decode(tokens)
print("Decoded Token:", my_token)