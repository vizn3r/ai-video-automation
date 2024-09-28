from llama_cpp import LLAMA_DEFAULT_SEED, LLAMA_POOLING_TYPE_UNSPECIFIED, LLAMA_ROPE_SCALING_TYPE_UNSPECIFIED, CreateChatCompletionResponse, Llama, LLAMA_SPLIT_MODE_LAYER
from flask import Flask, request

from typing import Any
import os
import json

from utils import Except, Info, Error

class LLMContext:
    def __init__(self) -> None:
        pass

    def load_model(self) -> str:
        Info("Loading model...")
        try:
            self.llama = Llama(
                model_path="../models/llm/"+self.params["model_name"],
                n_gpu_layers=self.params["n_gpu_layers"],
                split_mode=self.params["split_mode"],
                main_gpu=self.params["gpu"],
                tensor_split=self.params["tensor_split"],
                vocab_only=self.params["vocab_only"],
                use_mmap=self.params["use_nmap"],
                use_mlock=self.params["use_mlock"],
                kv_overrides=self.params["kv_overrides"],
                seed=self.params["seed"],
                n_ctx=self.params["ctx_size"],
                n_batch=self.params["batch_size"],
                n_threads=self.params["threads"],
                n_threads_batch=self.params["threads_batch"],
                rope_scaling_type=self.params["rope_scaling_type"],
                pooling_type=self.params["pooling_type"],
                rope_freq_base=self.params["rope_freq_base"],
                rope_freq_scale=self.params["rope_freq_scale"],
                yarn_ext_factor=self.params["yarn_ext_factor"],
                yarn_attn_factor=self.params["yarn_attr_factor"],
                yarn_beta_fast=self.params["yarn_beta_fast"],
                yarn_beta_slow=self.params["yarn_beta_slow"],
                yarn_orig_ctx=self.params["yarn_orig_ctx"],
                logits_all=self.params["logits_all"],
                embedding=self.params["embedding"],
                offload_kqv=self.params["offload_kqv"],
                last_n_tokens_size=self.params["last_n_token_size"],
                lora_base=self.params["lora_base"],
                lora_path=self.params["lora_path"],
                numa=self.params["numa"],
                chat_format=self.params["chat_format"],
                chat_handler=self.params["chat_handler"],
                draft_model=self.params["draft_model"],
                tokenizer=self.params["tokenizer"],
                verbose=DEBUG,
                type_k=self.params["type_k"],
                type_v=self.params["type_v"],
            )
        except Exception as e:
            Except(e, "Failed loading model")
            return "failed loading model"
        Info("Loaded model '", self.params["model_name"], "'")
        return "loaded model"

    def chat(self) -> CreateChatCompletionResponse | None:
        if self.llama == None:
            return None
        Info("Creating chat completion...")
        Debug("Chat:", llm.params["messages"])
        try:
            res = self.llama.create_chat_completion(
                messages=self.params["messages"],
                functions=self.params["functions"],
                function_call=self.params["function_call"],
                tools=self.params["tools"],
                tool_choice=self.params["tool_choice"],
                temperature=self.params["temperature"],
                top_p=self.params["top_p"],
                top_k=self.params["top_k"],
                min_p=self.params["min_p"],
                typical_p=self.params["typical_p"],
                stream=self.params["stream"],
                stop=self.params["stop"],
                seed=self.params["msg_seed"],
                response_format=self.params["response_format"],
                max_tokens=self.params["max_tokens"],
                presence_penalty=self.params["presence_penalty"],
                frequency_penalty=self.params["frequency_penalty"],
                repeat_penalty=self.params["repeat_penalty"],
                tfs_z=self.params["tfs_z"],
                mirostat_mode=self.params["mirostat_mode"],
                mirostat_tau=self.params["mirostat_tau"],
                mirostat_eta=self.params["mirostat_eta"],
                model=self.params["model"],
                logits_processor=self.params["logits_processor"],
                grammar=self.params["grammar"],
                logit_bias=self.params["logit_bias"],
            )
            Debug("Assistant response: " + res.__str__())
            if isinstance(res, dict):
                return res
            else:
                return None
        except Exception as e:
            Except(e, "Failed creating chat competion")
            return None

    def set_param(self, param: str, value: Any):
        Debug("Settng parameter " + param + ": " + value)
        self.params[param] = value

    llama: Llama | None = None
    params: dict[str, Any] = {
        # Llama default parameters
        "model_name": "", #model_path
        "n_gpu_layers": 8,
        "split_mode": LLAMA_SPLIT_MODE_LAYER,
        "gpu": 0, #main_gpu
        "tensor_split": None,
        "vocab_only": False,
        "use_nmap": True,
        "use_mlock": False,
        "kv_overrides": None,
        "seed": LLAMA_DEFAULT_SEED,
        "ctx_size": 2048, #n_ctx
        "batch_size": 512, #n_batch
        "threads": 4, #n_threads
        "threads_batch": None, #n_threads_batch
        "rope_scaling_type": LLAMA_ROPE_SCALING_TYPE_UNSPECIFIED,
        "pooling_type": LLAMA_POOLING_TYPE_UNSPECIFIED,
        "rope_freq_base": 0.0,
        "rope_freq_scale": 0.0,
        "yarn_ext_factor": -1.0,
        "yarn_attr_factor": 1.0,
        "yarn_beta_fast": 32.0,
        "yarn_beta_slow": 1.0,
        "yarn_orig_ctx": 0,
        "logits_all": False,
        "embedding": False,
        "offload_kqv": True,
        "last_n_token_size": 64,
        "lora_base": None,
        "lora_path": None,
        "numa": False,
        "chat_format": "chatml",
        "chat_handler": None,
        "draft_model": None,
        "tokenizer": None,
        "verbose": False,
        "type_k": None,
        "type_v": None,

        # Default params for chat completion
        "messages": None,
        "functions": None,
        "function_call": None,
        "tools": None,
        "tool_choice": None,
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "min_p": 0.05,
        "typical_p": 1.0,
        "stream": False,
        "stop": [],
        "msg_seed": None,
        "response_format": None,
        "max_tokens": None,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.0,
        "repeat_penalty": 1.1,
        "tfs_z": 1.0,
        "mirostat_mode": 0,
        "mirostat_tau": 5.0,
        "mirostat_eta": 0.1,
        "model": None,
        "logits_processor": None,
        "grammar": None,
        "logit_bias": None,

        "history": [],
    }

llm = LLMContext()
app = Flask(__name__)

@app.get("/")
def get():
    llms = os.listdir("../models/llm/")
    res = {
        "models": llms
    }
    return json.dumps(res)

@app.post("/")
def post():
    req = request.get_json()
    Debug("New POST req: ", req)
    for param in llm.params:
        try:
            Debug("Setting param", param, ":", req[param])
            llm.params[param] = req[param]
        except:
            pass
    if llm.llama == None and llm.params["model_name"] != "":
        llm.load_model()

    # completion system
    m = llm.params["messages"]
    if m == None:
        return "ok"
    # for single message and single response
    if isinstance(m, str):
        llm.params["messages"] = [{ "role": "user", "content": m }]
        out = llm.chat()
        if out == None or out["choices"].__len__() == 0 or out["choices"][0]["message"] == None:
            return "There is no response"
        msg = out["choices"][0]["message"]["content"]
        if out == None or msg == None:
            return "there is no response"
        else:
            return msg
    # for chat history
    llm.params["history"] = llm.params["history"] + m
    llm.params["messages"] = llm.params["history"]
    out = llm.chat()
    if out == None:
        return "there was no response"
    llm.params["history"] += [out["choices"][0]['message']]
    Debug("History:", llm.params["history"])
    return out
