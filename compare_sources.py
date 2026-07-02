import ast
import sys
from os.path import splitext

SKIP_EXTS = (".md", ".rst")


class RemoveDocstrings(ast.NodeTransformer):
    """
    Strips docstrings from source files so that they aren't used for comparing ASTs.
    """

    def visit(self, node: ast.AST) -> ast.AST:
        try:
            # remove docstrings from the files
            if ast.get_docstring(node) is not None:
                del node.body[0]
        except:
            pass
        return super().visit(node)


def sources_equal(src1: str, src2: str) -> bool:
    """
    Compare Python source files at the AST level without docstrings or comments. If two files are equal except for
    changes to docstrings or comments, they will be considered equal by this function. Any other changes will appear
    as differences in the AST representations, which are compared inefficiently by dumping parts of the tree to string
    representations and compared.
    """
    remdoc = RemoveDocstrings()

    m1: ast.Module = remdoc.generic_visit(ast.parse(src1))
    m2: ast.Module = remdoc.generic_visit(ast.parse(src2))

    list1 = list(ast.walk(m1))
    list2 = list(ast.walk(m2))

    if len(list1) != len(list2):
        return False

    # TODO: more efficient way than using ast.dump?
    return all(type(n1) is type(n2) and ast.dump(n1) == ast.dump(n2) for n1, n2 in zip(list1, list2))


def files_considered_equal(file1: str, file2: str) -> bool:
    """
    Returns True if the files are considered equal, that is they are doc files or differ only in docstrings or comments.
    """
    _, ext1 = splitext(file1)
    _, ext2 = splitext(file2)

    # if extensions aren't equal then definitely different (which shouldn't happen anyway)
    if ext1 != ext2:
        return False

    # if extensions are an ignored type, ie. docs, don't compare at all
    if ext1 in SKIP_EXTS:
        return True

    # if not Python source files, they aren't doc files at this point so assume different
    if ext1 != ".py":
        return False

    # compare the actual parsed contents of the source files
    with open(file1) as o1, open(file2) as o2:
        return sources_equal(o1.read(), o2.read())


if __name__ == "__main__":
    _, file1, file2 = sys.argv
    sys.exit(0 if files_considered_equal(file1, file2) else 1)
