from __future__ import annotations

from olca import schema

from typing import Callable, List, Tuple


class ProcessProduct:

    def __init__(self, process: schema.Ref, flow: schema.Ref):
        self.process = process
        self.flow = flow

    @staticmethod
    def from_json(json: dict):
        process = None
        process_dict = json.get('process')
        if process_dict is not None:
            process = schema.Ref.from_json(process_dict)
        flow = None
        flow_dict = json.get('flow')
        if flow_dict is not None:
            flow = schema.Ref.from_json(flow_dict)
        return ProcessProduct(process, flow)


class UpstreamNode:

    def __init__(self, product: ProcessProduct, result=0.0):
        self.product = product
        self.result = result
        self.childs: List[UpstreamNode] = []

    @staticmethod
    def from_json(json: dict) -> UpstreamNode:
        product = None
        product_dict = json.get('product')
        if product_dict is not None:
            product = ProcessProduct.from_json(product_dict)
        result = json.get('result', 0.0)
        node = UpstreamNode(product, result)
        childs: List[dict] = json.get('childs')
        if childs is not None:
            for child in childs:
                node.childs.append(UpstreamNode.from_json(child))
        return node


class UpstreamTree:

    def __init__(self, ref: schema.Ref, root: UpstreamNode):
        self.ref = ref
        self.root = root

    @staticmethod
    def from_json(json: dict) -> UpstreamTree:
        ref = None
        ref_dict = json.get('ref')
        if ref_dict is not None:
            ref = schema.Ref.from_json(ref_dict)
        root = None
        root_dict = json.get('root')
        if root_dict is not None:
            root = UpstreamNode.from_json(root_dict)
        return UpstreamTree(ref, root)

    def traverse(self, fn: Callable[[Tuple[UpstreamNode, int]], None]):

        def traverse_(parent: UpstreamNode, depth: int):
            if not parent:
                return
            fn((parent, depth))
            if parent.childs:
                for child in parent.childs:
                    traverse_(child, depth + 1)

        traverse_(self.root, 0)
