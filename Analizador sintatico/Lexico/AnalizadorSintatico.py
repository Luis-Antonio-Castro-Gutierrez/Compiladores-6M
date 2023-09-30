import re
import tkinter as tk
from tkinter import messagebox
from ply import lex, yacc

tokens = (
        'FOR',
        'INT',
        'ID',
        'NUM',
        'STRING',
        'PLUS',
        'SEMICOLON',
        'LPAREN',
        'RPAREN',
        'LBRACE',
        'RBRACE',
        'DOT',
        'EQUALS',
        'LEQ'
)
t_PLUS = r'\+'
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_DOT = r'\.'
t_EQUALS = r'='
t_LEQ = r'<='

def t_STRING(t):
        r'\".*?\"'
        t.value  = t.value[1:-1]
        return t

def t_ID(t):
        r'[a-zA-Z][a-zA-Z0-9]*'
        if t.value == 'for':
                t.type = 'FOR'
        elif t.value == 'int':
                t.type = 'INT'
        return t

def t_NUM(t):
        r'\d+'
        t.value = int(t.value)
        return  t

t_ignore = '\t\n'

def t_error(t):
    error_message(f"Token desconocido '{t.value[0]}'", t.lineno)
    t.lexer.skip(1)

lexer = lex.lex()

def p_for_loop(p):
        '''for_loop : FOR INT ID EQUALS NUM SEMICOLON ID LEQ NUM SEMICOLON ID PLUS  '''
        pass

def p_error(p):
        if p:
                error_message(f"Error de sintaxis en '{p.value}'",p.lineo)
        else:
                error_message(f"Error de sintaxis: final inesperado en el codigo ", len(code_text.get("1.0", "end-1c").split('\n')))

parser = yacc.yacc()

def lex_analyzer(code):
        lexer.input(code)
        tokens = []
        while True:
                token = lexer.token()
                if not token:
                        break
                tokens.append((token.lineno, token.type, token.value))
        return tokens

def parse_code(code):
        parser.parse(code, lexer = lexer)

def error_message(message, line_number):
        messagebox.showerror("Error de sintaxis", f"{message}\nEn la linea {line_number}")

def process_code():
        code = code_text.get("1.0", "end-1c")
        tokens = lex_analyzer(code)
        result_text.delete("1.0", "end")
        for token in tokens:
                line_number, token_type, token_value = token
                result_text.insert("end", f"Linea->: {token_type}->{token_value}\n")
        parse_code(code)

window = tk.Tk()
window.title("Lexer")
window.geometry("600x400")

code_label = tk.Label(window, text="Ingrese el código")
code_label.pack()

code_text = tk.Text(window, height=10, width=50)
code_text.pack()

process_button = tk.Button(window, text="Precesar", command=process_code)
process_button.pack()

result_label = tk.Label(window, text="Tokens:")
result_label.pack()

result_text = tk.Text(window, height=50, width=50)
result_text.pack()

window.mainloop()