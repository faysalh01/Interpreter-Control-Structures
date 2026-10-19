# Onyx Part 4 – Complete Parser and Interpreter Grammar

The following grammar describes the syntax supported by the Onyx Part 4 Interpreter.

<program> ::= { <statement> }

<statement> ::= <assignment>
              | <print-statement>
              | <if-statement>
              | <while-statement>

<assignment> ::= "let" <identifier> "=" <expression> ";"
               | <identifier> "=" <expression> ";"

<print-statement> ::= "print" "(" <expression> ")" ";"

<if-statement> ::= "if" "(" <expression> ")" "{" <program> "}"
                   [ "else" "{" <program> "}" ]

<while-statement> ::= "while" "(" <expression> ")" "{" <program> "}"

<expression> ::= <comparison-expr>

<comparison-expr> ::= <arithmetic-expr> [ <comparison-operator> <arithmetic-expr> ]

<arithmetic-expr> ::= <term> { ("+" | "-") <term> }

<term> ::= <factor> { ("*" | "/") <factor> }

<factor> ::= <number>
           | <identifier>
           | "(" <expression> ")"

<comparison-operator> ::= "==" | "!=" | "<" | ">" | "<=" | ">="

<identifier> ::= [a-zA-Z_] { [a-zA-Z0-9_] }

<number> ::= [0-9] { [0-9] }
