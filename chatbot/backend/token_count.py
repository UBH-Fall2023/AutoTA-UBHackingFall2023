import tiktoken

def count_tokens(text: str) -> int:
   """Counts the number of tokens in a text string."""
   encoding = tiktoken.encoding_for_model("gpt-4")
   tokens = encoding.encode(text)
   return len(tokens)

