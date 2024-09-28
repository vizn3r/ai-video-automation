# Source: https://github.com/vizn3r/ai-toolkit/blob/main/proc/llm.py

from llama_cpp import LLAMA_DEFAULT_SEED, LLAMA_POOLING_TYPE_UNSPECIFIED, LLAMA_ROPE_SCALING_TYPE_UNSPECIFIED, CreateChatCompletionResponse, Llama, LLAMA_SPLIT_MODE_LAYER
from typing import Any
import os
from utils import Except, Info, Error, END
import warnings

if __name__ == "__main__":
    Error("This script is not meant to run standalone")
    exit(0)

LLM_PATH = os.environ["LLM_PATH"] or "../../media/llm/model.gguf"

warnings.filterwarnings("ignore", category=FutureWarning)

class LLMContext:
    def __init__(self) -> None:
        pass

    def load_model(self):
        Info("Loading model")
        if self.llama != None:
            Info("Model already loaded")
            return self
        try:
            self.llama = Llama(
                model_path=self.params["model_name"],
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
                type_k=self.params["type_k"],
                type_v=self.params["type_v"],
            )
        except Exception as e:
            Except(e, "Failed loading model")
            return None
        Info("Loaded model '", self.params["model_name"], "'")
        return self

    def chat(self) -> CreateChatCompletionResponse | None:
        if self.llama == None:
            return None
        Info("Creating chat completion")
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
                logit_bias=self.params["logit_bias"]
            )
            if isinstance(res, dict):
                return res
            else:
                return None
        except Exception as e:
            Except(e, "Failed creating chat competion")
            return None

    def set_param(self, param: str, value: Any):
        self.params[param] = value

    llama: Llama | None = None
    params: dict[str, Any] = {
        # Llama default parameters
        "model_name": LLM_PATH, #model_path
        "n_gpu_layers": 8,
        "split_mode": LLAMA_SPLIT_MODE_LAYER,
        "gpu": 0, #main_gpu
        "tensor_split": None,
        "vocab_only": False,
        "use_nmap": True,
        "use_mlock": False,
        "kv_overrides": None,
        "seed": LLAMA_DEFAULT_SEED,
        "ctx_size": 2096, #n_ctx
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

        
class RedditVideo:
    def title(subreddit, post_title, post_content):
        llm = LLMContext()
        llm.load_model()
        message = [
            {
                "role": "user",
                "content": f"Generate a catchy, SEO-optimized, and clickbait-style video title based on the subreddit '{subreddit}', post title '{post_title}', and post content '{post_content}'. The title must be engaging and under 100 characters in length. Respond with ONLY one title and no additional text."
            }
        ]
        llm.set_param("messages", message)
        llm.set_param("ctx_size", len(message[0]["content"]) + llm.params["ctx_size"])
        out = llm.chat()
        if out == None or out["choices"].__len__() == 0 or out["choices"][0]["message"] == None:
            return "There is no response"
        msg = out["choices"][0]["message"]["content"]
        if len(msg) >= 100:
            Info("Video title is too long, redoing it recursively")
            llm.llama.close()
            msg = RedditVideo.title(subreddit, post_title, post_content)
        Info("Video title:", END, msg)
        llm.llama.close()
        return msg

    def description(subreddit, post_title, post_content):
        llm = LLMContext()
        llm.load_model()
        message = [
            {
                "role": "user",
                "content": f"Generate an engaging video description using the subreddit '{subreddit}', post title '{post_title}', and post content '{post_content}'. Respond ONLY with the video description and nothing else. Do not include a title."
            }
        ]
        llm.set_param("messages", message)
        llm.set_param("ctx_size", len(message[0]["content"]) + llm.params["ctx_size"])
        out = llm.chat()
        if out == None or out["choices"].__len__() == 0 or out["choices"][0]["message"] == None:
            return "There is no response"
        msg = out["choices"][0]["message"]["content"]
        Info("Video description:", END, msg)
        llm.llama.close()
        return msg

    def tags(subreddit, post_title, post_content):
        llm = LLMContext()
        llm.load_model()
        message = [
            {
                "role": "user",
                "content": f"Generate video tags based on the subreddit '{subreddit}', post title '{post_title}', and post content '{post_content}'. Respond ONLY with the video tags in one line, separated by commas, and **without any hashtags, spaces, or whitespace**. Include tags related to Reddit and the title of the subreddit. Generate AT LEAST 50 tags. Do not respond with anything else."
            }
        ]
        llm.set_param("messages", message)
        llm.set_param("ctx_size", len(message[0]["content"]) + llm.params["ctx_size"])
        out = llm.chat()
        if out == None or out["choices"].__len__() == 0 or out["choices"][0]["message"] == None:
            return "There is no response"
        msg = out["choices"][0]["message"]["content"]
        Info("Video tags:", END, msg)
        llm.llama.close()
        return msg

# data = get_hot_post_data("stories")
# generate_reddit_video_title(data["subreddit"], data["title"], data["content"])
# generate_reddit_video_description(data["subreddit"], data["title"], data["content"])
# generate_reddit_video_tags(data["subreddit"], data["title"], data["content"])

# app = Flask(__name__)
# 
# @app.get("/")
# def get():
#     llms = os.listdir("../models/llm/")
#     res = {
#         "models": llms
#     }
#     return json.dumps(res)
# 
# @app.post("/")
# def post():
#     req = request.get_json()
#     for param in llm.params:
#         try:
#             llm.params[param] = req[param]
#         except:
#             pass
#     if llm.llama == None and llm.params["model_name"] != "":
#         llm.load_model()
# 
#     # completion system
#     m = llm.params["messages"]
#     if m == None:
#         return "ok"
#     # for single message and single response
#     if isinstance(m, str):
#         llm.params["messages"] = [{ "role": "user", "content": m }]
#         out = llm.chat()
#         if out == None or out["choices"].__len__() == 0 or out["choices"][0]["message"] == None:
#             return "There is no response"
#         msg = out["choices"][0]["message"]["content"]
#         if out == None or msg == None:
#             return "there is no response"
#         else:
#             return msg
#     # for chat history
#     llm.params["history"] = llm.params["history"] + m
#     llm.params["messages"] = llm.params["history"]
#     out = llm.chat()
#     if out == None:
#         return "there was no response"
#     llm.params["history"] += [out["choices"][0]['message']]
#     return out
# 
# app.run(port=8080)