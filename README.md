# Onyx Programming Language - Control Structures & Interpreter

## Overview
This repository contains the complete implementation of the Onyx programming language interpreter. The interpreter supports variable declarations, arithmetic expressions, relational comparisons, conditional execution (`if`/`else`), and iteration (`while` loops).

---

## Architecture & Structure
The project is structured into distinct compiler/interpreter pipeline phases:

* `lexer.py`: Tokenizes raw source code into structured lexical tokens.
* `parser.py`: Parses tokens into an Abstract Syntax Tree (AST) using recursive descent parsing.
* `ast_nodes.py`: Defines the AST node classes representing expressions, statements, and control flow nodes.
* `interpreter.py`: Executes the AST, managing variable environments and evaluating operations and control structures.
* `run_tests.py`: Automated test runner script that executes all test files stored in the `tests/` directory.

---

## Formal Grammar Specification (EBNF)

```ebnf
Program         ::= StatementList ;
StatementList   ::= { Statement } ;

Statement       ::= VarDecl
                  | Assignment
                  | PrintStmt
                  | IfStmt
                  | WhileStmt ;

VarDecl         ::= "let" Identifier "=" Expression ";" ;
Assignment      ::= Identifier "=" Expression ";" ;
PrintStmt       ::= "print" "(" Expression ")" ";" ;

IfStmt          ::= "if" "(" Expression ")" "{" StatementList "}" [ "else" "{" StatementList "}" ] ;
WhileStmt       ::= "while" "(" Expression ")" "{" StatementList "}" ;

Expression      ::= EqualityExpr ;
EqualityExpr    ::= RelationalExpr { ( "==" | "!=" ) RelationalExpr } ;
RelationalExpr  ::= AdditiveExpr { ( "<" | "<=" | ">" | ">=" ) AdditiveExpr } ;
AdditiveExpr    ::= MultiplicativeExpr { ( "+" | "-" ) MultiplicativeExpr } ;
MultiplicativeExpr ::= Primary { ( "*" | "/" ) Primary } ;
Primary         ::= Number | Identifier | "(" Expression ")" ;
