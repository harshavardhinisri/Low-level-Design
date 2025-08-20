class Node:
    def __init__(self, name):
        self.name = name
        self.isFile = False

class File(Node):
    def __init__(self, name, content=""):
        super().__init__(name)
        self.isFile = True
        self.content = content

class Directory(Node):
    def __init__(self, name):
        super().__init__(name)
        self.children = {}  # name -> Node

class FileSystem:
    def __init__(self):
        self.root = Directory("/")

    def _traverse(self, path):
        if path == "/":
            return self.root
        parts = path.strip("/").split("/")
        node = self.root
        for part in parts:
            if part not in node.children:
                return None
            node = node.children[part]
        return node

    def mkdir(self, path):
        parts = path.strip("/").split("/")
        node = self.root
        for part in parts:
            if part not in node.children:
                node.children[part] = Directory(part)
            node = node.children[part]

    def addFile(self, path, content):
        parts = path.strip("/").split("/")
        filename = parts[-1]
        dir_path = parts[:-1]
        node = self.root
        for part in dir_path:
            if part not in node.children:
                node.children[part] = Directory(part)
            node = node.children[part]
        node.children[filename] = File(filename, content)

    def readFile(self, path):
        node = self._traverse(path)
        if node and node.isFile:
            return node.content
        return None

    def ls(self, path):
        node = self._traverse(path)
        if node.isFile:
            return [node.name]
        return sorted(node.children.keys())

fs = FileSystem()
fs.mkdir("/a/b/c")
fs.addFile("/a/b/c/file.txt", "Hello World")
print(fs.readFile("/a/b/c/file.txt"))  # Hello World
print(fs.ls("/a/b"))                   # ['c']
print(fs.ls("/a/b/c/file.txt"))        # ['file.txt']
