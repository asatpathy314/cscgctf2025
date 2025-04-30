from llama_cpp import Llama
import pprint

def complete(prefix):
    resp = llm.create_completion(
        prompt=prefix,
        max_tokens=1,
        temperature=0, 
    )
    pprint.pprint(resp)
    return prefix + resp["choices"][0]["text"]
  
if __name__ == "__main__":
    llm = Llama(model_path="./flaig_checker.gguf", logits_all=True)
    flag = "CSCG{"
    while not flag.endswith("}"):
        flag = complete(flag)
        print(f"Intermediate Flag: {flag}")

    print(f"Flag is: {flag}")