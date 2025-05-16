from comfy_execution.graph_utils import GraphBuilder


class TestCustomNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process"
    CATEGORY = "custom"

    def process(self, text):
        # 初始化执行图
        graph = GraphBuilder()
        nodes = {}

        # 固定参数配置
        # 1. 加载checkpoint
        nodes["checkpoint"] = graph.node(
            class_type="CheckpointLoaderSimple",
            ckpt_name="v1-5-pruned-emaonly-fp16.safetensors",
        )

        # 2. 生成空latent
        nodes["latent"] = graph.node(
            class_type="EmptyLatentImage", width=512, height=512, batch_size=1
        )

        # 3. 文本编码
        nodes["clip"] = graph.node(
            class_type="CLIPTextEncode", text=text, clip=nodes["checkpoint"].out(1)
        )

        # 4. 采样
        nodes["sampler"] = graph.node(
            class_type="KSampler",
            seed=156680208700286,
            steps=20,
            cfg=8,
            sampler_name="euler",
            scheduler="normal",
            denoise=1,
            model=nodes["checkpoint"].out(0),
            positive=nodes["clip"].out(0),
            negative=nodes["clip"].out(0),  # 简化处理，使用相同提示词
            latent_image=nodes["latent"].out(0),
        )

        # 5. VAE解码
        nodes["vae"] = graph.node(
            class_type="VAEDecode",
            samples=nodes["sampler"].out(0),
            vae=nodes["checkpoint"].out(2),
        )

        return {
            "result": (nodes["vae"].out(0),),
            "expand": graph.finalize(),
        }
