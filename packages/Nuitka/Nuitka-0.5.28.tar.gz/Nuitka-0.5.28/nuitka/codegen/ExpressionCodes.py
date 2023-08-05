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
""" Expression codes, side effects, or statements that are an unused expression.

When you write "f()", i.e. you don't use the return value, that is an expression
only statement.

"""

from .CodeHelpers import generateExpressionCode
from .ErrorCodes import getReleaseCode


def generateExpressionOnlyCode(statement, emit, context):
    return getStatementOnlyCode(
        value   = statement.getExpression(),
        emit    = emit,
        context = context
    )


def getStatementOnlyCode(value, emit, context):
    tmp_name = context.allocateTempName(
        base_name = "unused",
        type_name = "NUITKA_MAY_BE_UNUSED PyObject *",
        unique    = True
    )

    # An error of the expression is dealt inside of this, not necessary here.
    generateExpressionCode(
        expression = value,
        to_name    = tmp_name,
        emit       = emit,
        context    = context
    )

    getReleaseCode(
        release_name = tmp_name,
        emit         = emit,
        context      = context
    )


def generateSideEffectsCode(to_name, expression, emit, context):
    for side_effect in expression.getSideEffects():
        getStatementOnlyCode(
            value   = side_effect,
            emit    = emit,
            context = context
        )

    generateExpressionCode(
        to_name    = to_name,
        expression = expression.getExpression(),
        emit       = emit,
        context    = context
    )
