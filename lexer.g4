lexer grammar ExprLexer;

INCLUDE: 'include';
MUST : 'must';
WHILE : 'while' ;
PREDATES: 'predates';
CAN: 'can';
CAN_CONTROL: 'can control';
HAVE_FUEL: 'have fuel';
FIRE: 'fire';

COMMA: ',';
SEMICOLON: ';';

ID: [a-zA-Z_][a-zA-Z_0-9]*;
TANK: [0-9]+;
WS: [ \t\n\r\f]+ -> skip ;