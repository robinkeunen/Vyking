









































_allowed = {
    ('NOT', TY_BOOL),
    (TY_BOOL,   'AND', TY_BOOL),
    (TY_BOOL,   'OR', TY_BOOL),
    (TY_INT,    'EQ', TY_INT),
    (TY_FLOAT,  'EQ', TY_FLOAT),
    (TY_BOOL,   'EQ', TY_BOOL),
    (TY_STRING, 'EQ', TY_STRING),
    (TY_FUNC,   'EQ', TY_FUNC),
    (TY_VOID,   'EQ', TY_VOID),
    (TY_RT,     'EQ', TY_RT),
    (TY_INT,    'NEQ', TY_INT),
    (TY_FLOAT,  'NEQ', TY_FLOAT),
    (TY_BOOL,   'NEQ', TY_BOOL),
    (TY_STRING, 'NEQ', TY_STRING),
    (TY_FUNC,   'NEQ', TY_FUNC),
    (TY_VOID,   'NEQ', TY_VOID),
    (TY_RT,     'NEQ', TY_RT),
    (TY_INT,    'LEQ', TY_INT),
    (TY_FLOAT,  'LEQ', TY_FLOAT),
    (TY_FLOAT,  'LEQ', TY_INT),
    (TY_INT,    'LEQ', TY_FLOAT),
    (TY_INT,    'GEQ', TY_INT),
    (TY_FLOAT,  'GEQ', TY_FLOAT),
    (TY_FLOAT,  'GEQ', TY_INT),
    (TY_INT,    'GEQ', TY_FLOAT),
    (TY_INT,    'LT', TY_INT),
    (TY_FLOAT,  'LT', TY_FLOAT),
    (TY_FLOAT,  'LT', TY_INT),
    (TY_INT,    'LT', TY_FLOAT),
    (TY_INT,    'GT', TY_INT),
    (TY_FLOAT,  'GT', TY_FLOAT),
    (TY_FLOAT,  'GT', TY_INT),
    (TY_INT,    'GT', TY_FLOAT),
    (TY_INT,    'PLUS', TY_INT),
    (TY_FLOAT,  'PLUS', TY_FLOAT),
    (TY_FLOAT,  'PLUS', TY_INT),
    (TY_INT,    'PLUS', TY_FLOAT),
    (TY_INT,    'MINUS', TY_INT),
    (TY_FLOAT,  'MINUS', TY_FLOAT),
    (TY_FLOAT,  'MINUS', TY_INT),
    (TY_INT,    'MINUS', TY_FLOAT),
    (TY_INT,    'TIMES', TY_INT),
    (TY_FLOAT,  'TIMES', TY_FLOAT),
    (TY_FLOAT,  'TIMES', TY_INT),
    (TY_INT,    'TIMES', TY_FLOAT),
    (TY_INT,    'DIVIDE', TY_INT),
    (TY_FLOAT,  'DIVIDE', TY_FLOAT),
    (TY_FLOAT,  'DIVIDE', TY_INT),
    (TY_INT,    'DIVIDE', TY_FLOAT),
    (TY_STRING, 'PLUS', TY_STRING),
    ('UMINUS', TY_INT),
    ('UNMINUS', TY_FLOAT),
}
