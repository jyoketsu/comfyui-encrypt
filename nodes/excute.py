import requests
import json


# 通过 HTTP 调用本地 ComfyUI 服务
def execute_workflow(workflow):
    response = requests.post("http://localhost:8188/prompt", json={"prompt": workflow})
    prompt_id = response.json()["prompt_id"]

    # 轮询获取结果
    while True:
        history = requests.get(f"http://localhost:8188/history/{prompt_id}").json()
        if prompt_id in history:
            outputs = history[prompt_id]["outputs"]
            if "8" in outputs:  # 假设节点8是最终输出
                return outputs["8"]["images"][0]
