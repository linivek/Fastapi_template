"""
Flake8插件 - 受保护文件

此插件检测可能导致文件意外删除的代码操作。
"""

import ast
import os
from typing import Any, Dict, Generator, List, Tuple, Type

# 受保护的文件和目录列表
PROTECTED_FILES = [
    # 配置文件
    "pyproject.toml",
    "poetry.lock",
    ".env",
    ".env.example",
    "alembic.ini",
    "Dockerfile",
    "docker-compose.yml",
    "Makefile",
    ".flake8",
    ".gitignore",
    ".pre-commit-config.yaml",
    # 重要目录
    "app/",
    "alembic/versions/",
    "tests/",
]

# 危险的文件操作函数
DANGEROUS_FUNCTIONS = [
    # 标准库
    "os.remove",
    "os.unlink",
    "os.rmdir",
    "os.removedirs",
    "shutil.rmtree",
    # 路径库
    "pathlib.Path.unlink",
    "pathlib.Path.rmdir",
    # 简化形式
    "remove",
    "unlink",
    "rmdir",
    "rmtree",
]


class ProtectedFilesVisitor(ast.NodeVisitor):
    """AST访问者，用于检测可能删除受保护文件的操作。"""

    def __init__(self, filename: str):
        self.filename = filename
        self.errors: List[Tuple[int, int, str]] = []

    def visit_Call(self, node: ast.Call) -> None:
        """
        访问函数调用节点，检测删除文件操作。

        Args:
            node: AST函数调用节点
        """
        # 检查是否是危险函数调用
        func_name = self._get_func_name(node.func)
        if func_name in DANGEROUS_FUNCTIONS:
            # 尝试获取文件路径参数
            if node.args:
                arg = node.args[0]
                file_path = self._extract_path(arg)
                if file_path:
                    # 检查是否是受保护的文件
                    for protected in PROTECTED_FILES:
                        if (
                            file_path == protected
                            or file_path.startswith(protected)
                            or protected in file_path
                        ):
                            self.errors.append(
                                (
                                    node.lineno,
                                    node.col_offset,
                                    f"FPF100 Attempting to delete protected file: {file_path} with {func_name}()",
                                )
                            )
            else:
                # 如果无法确定文件路径，也发出警告
                self.errors.append(
                    (
                        node.lineno,
                        node.col_offset,
                        f"FPF101 Potentially dangerous file operation detected: {func_name}()",
                    )
                )

        # 继续访问子节点
        self.generic_visit(node)

    def _get_func_name(self, node: ast.expr) -> str:
        """
        从AST节点提取函数名。

        Args:
            node: AST表达式节点

        Returns:
            函数名字符串
        """
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            obj_name = self._get_func_name(node.value)
            return f"{obj_name}.{node.attr}" if obj_name else node.attr
        return ""

    def _extract_path(self, node: ast.expr) -> str:
        """
        从AST节点提取文件路径。

        Args:
            node: AST表达式节点

        Returns:
            文件路径字符串
        """
        if isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        elif isinstance(node, ast.JoinedStr):
            # f-strings
            parts = []
            for value in node.values:
                if isinstance(value, ast.Str) or (
                    isinstance(value, ast.Constant) and isinstance(value.value, str)
                ):
                    parts.append(value.s if hasattr(value, "s") else value.value)
                else:
                    parts.append("<dynamic>")
            return "".join(parts)
        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            # 字符串连接
            left = self._extract_path(node.left)
            right = self._extract_path(node.right)
            if left and right:
                return left + right
        return ""


class ProtectedFilesPlugin:
    """Flake8插件，用于检测可能删除受保护文件的操作。"""

    name = "flake8-protected-files"
    version = "0.1.0"

    def __init__(self, tree: ast.AST, filename: str):
        self.tree = tree
        self.filename = filename

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        """
        运行插件检查。

        Yields:
            错误元组 (行号, 列号, 消息, 类型)
        """
        visitor = ProtectedFilesVisitor(self.filename)
        visitor.visit(self.tree)

        for line, col, message in visitor.errors:
            yield line, col, message, type(self)
