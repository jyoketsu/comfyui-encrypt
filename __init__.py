from .nodes.decrypt_node import DecodeCryptoNode

# 注册节点
NODE_CLASS_MAPPINGS = {"DecodeCryptoNode": DecodeCryptoNode}
NODE_DISPLAY_NAME_MAPPINGS = {"DecodeCryptoNode": "🔓工作流解密器"}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
