from .nodes.test_custom_node import TestCustomNode

# 注册节点
NODE_CLASS_MAPPINGS = {"TestCustomNode": TestCustomNode}
NODE_DISPLAY_NAME_MAPPINGS = {"TestCustomNode": "测试自定义节点"}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
