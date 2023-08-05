#     Copyright 2017, Kay Hayen, mailto:kay.hayen@gmail.com
#
#     Part of "Nuitka", an optimizing Python compiler that is compatible and
#     integrates with CPython, but also works on its own.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
""" Operations on the tree.

This is mostly for the different kinds of visits that the node tree can have.
You can visit a scope, a tree (module), or every scope of a tree (module).

"""

def visitTree(tree, visitor):
    visitor.onEnterNode(tree)

    for visitable in tree.getVisitableNodes():
        if visitable is None:
            raise AssertionError(
                "'None' child encountered",
                tree,
                tree.source_ref
            )

        visitTree(visitable, visitor)

    visitor.onLeaveNode(tree)


def visitFunction(function, visitor):
    visitor.onEnterNode(function)
    visitor.onLeaveNode(function)


def visitModule(module, visitor):
    visitor.onEnterNode(module)
    visitor.onLeaveNode(module)


class VisitorNoopMixin(object):
    def onEnterNode(self, node):
        """ Overloaded for operation before the node children were done. """
        pass

    def onLeaveNode(self, node):
        """ Overloaded for operation after the node children were done. """
        pass
