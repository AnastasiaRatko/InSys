parser grammar ExprParser;
options { tokenVocab=ExprLexer; }

game: rules+;

rules
    : includeRule
    | canRule
    | canControlRule
    | predatesRule
    | mustRule
    | haveFuelRule
    | fireRule
    ;

includeRule : ID INCLUDE list_id;

canRule : list_id CAN list_id;

canControlRule: ID CAN_CONTROL list_id;

predatesRule : ID PREDATES ID;

mustRule : list_id MUST list_id WHILE ID;

haveFuelRule : ID HAVE_FUEL TANK;

fireRule : ID FIRE ID;

list_id: ID (COMMA ID)* ;
