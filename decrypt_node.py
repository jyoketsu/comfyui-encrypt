class AlwaysEqualProxy(str):
    def __eq__(self, _):
        return True

    def __ne__(self, _):
        return False


class AlwaysTupleZero(tuple):
    def __getitem__(self, _):
        return AlwaysEqualProxy(super().__getitem__(0))


class DecodeCryptoNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "key": ("STRING", {"default": "", "multiline": False}),
                "encrypt_api_data": ("STRING", {"default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    # RETURN_TYPES = AlwaysTupleZero(AlwaysEqualProxy("*"))
    RETURN_NAMES = ("image",)
    FUNCTION = "decrypt"
    CATEGORY = "Custom Nodes"

    def decrypt(self, key, encrypt_api_data):
        print(f"key: {key}")
        print(f"encrypt_api_data: {encrypt_api_data}")

        testJsonData = {
            "3": {
                "inputs": {
                    "seed": 156680208700286,
                    "steps": 20,
                    "cfg": 8,
                    "sampler_name": "euler",
                    "scheduler": "normal",
                    "denoise": 1,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["5", 0],
                },
                "class_type": "KSampler",
                "_meta": {"title": "K采样器"},
            },
            "4": {
                "inputs": {"ckpt_name": "v1-5-pruned-emaonly-fp16.safetensors"},
                "class_type": "CheckpointLoaderSimple",
                "_meta": {"title": "Checkpoint加载器（简易）"},
            },
            "5": {
                "inputs": {"width": 512, "height": 512, "batch_size": 1},
                "class_type": "EmptyLatentImage",
                "_meta": {"title": "空Latent图像"},
            },
            "6": {
                "inputs": {
                    "text": "beautiful scenery nature glass bottle landscape, , purple galaxy bottle,",
                    "speak_and_recognation": {"__value__": [False, True]},
                    "clip": ["4", 1],
                },
                "class_type": "CLIPTextEncode",
                "_meta": {"title": "CLIP文本编码"},
            },
            "7": {
                "inputs": {
                    "text": "text, watermark",
                    "speak_and_recognation": {"__value__": [False, True]},
                    "clip": ["4", 1],
                },
                "class_type": "CLIPTextEncode",
                "_meta": {"title": "CLIP文本编码"},
            },
            "8": {
                "inputs": {"samples": ["3", 0], "vae": ["4", 2]},
                "class_type": "VAEDecode",
                "_meta": {"title": "VAE解码"},
            },
        }

        # 将测试数据替换为实际加密数据（待实现解密逻辑）
        workflow_data = testJsonData  # 这里应该替换为解密后的数据

        # 创建执行上下文
        from comfy import PromptExecutor

        executor = PromptExecutor()

        # 执行工作流并获取结果
        outputs, _ = executor.execute(workflow_data, {})

        # 提取最终VAE解码后的图像数据（对应节点8的输出）
        return (outputs["8"][0],)  # 返回元组格式的IMAGE类型


# 注册节点
NODE_CLASS_MAPPINGS = {"DecodeCryptoNode": DecodeCryptoNode}
NODE_DISPLAY_NAME_MAPPINGS = {"DecodeCryptoNode": "🔓工作流解密器"}
