#!/usr/bin/env python
import sys
import ply.lex as lex
import ply.yacc as yacc
import lexer


rules_store = []
# Section 19.2

def p_Goal(p):
    '''Goal : CompilationUnit'''
    rules_store.append(p.slice)

# Section 19.3

def p_Literal(p):
    ''' Literal : INT_CONSTANT
    | FLOAT_CONSTANT
    | CHAR_CONSTANT
    | STR_CONSTANT
    | NULL
    '''
    rules_store.append(p.slice)


# Section 19.4

def p_Type(p):
    ''' Type : PrimitiveType
    | ReferenceType
    '''
    rules_store.append(p.slice)

def p_PrimitiveType(p):
    ''' PrimitiveType : NumericType
    | BOOLEAN
    '''
    rules_store.append(p.slice)

def p_NumericType(p):
    ''' NumericType : IntegralType
    | FloatingPointType
    '''
    rules_store.append(p.slice)

def p_IntegralType(p):
    ''' IntegralType : BYTE
    | SHORT
    | INT
    | LONG
    | CHAR
    '''
    rules_store.append(p.slice)

def p_FloatingPointType(p):
    ''' FloatingPointType : FLOAT
    | DOUBLE
    '''
    rules_store.append(p.slice)

def p_ReferenceType(p):
    ''' ReferenceType : ArrayType
    | ClassType
    '''
    rules_store.append(p.slice)

def p_ClassType(p):
    '''
    ClassType : Name
    '''
    rules_store.append(p.slice)

def p_ArrayType(p):
    ''' ArrayType : PrimitiveType L_SQBR R_SQBR
    | Name L_SQBR R_SQBR
    | ArrayType L_SQBR R_SQBR
    '''
    rules_store.append(p.slice)

# Section 19.5

def p_Name(p):
    ''' Name : SimpleName
    | QualifiedName'''
    rules_store.append(p.slice)

def p_SimpleName(p):
    ''' SimpleName : IDENTIFIER'''
    rules_store.append(p.slice)
    p[0] = {
        'idVal' : p[1],
        'isnotjustname' : False
        }
def p_QualifiedName(p):
    ''' QualifiedName : Name DOT IDENTIFIER'''
    rules_store.append(p.slice)
    p[0]= {
        'idVal' : p[1]['idVal']+"."+p[3]
        }

# Section 19.6

def p_CompilationUnit(p):
    '''
    CompilationUnit : PackageDeclaration ImportDeclarations TypeDeclarations
    | PackageDeclaration ImportDeclarations
    | PackageDeclaration TypeDeclarations
    | ImportDeclarations TypeDeclarations
    | PackageDeclaration
    | ImportDeclarations
    | TypeDeclarations
    |
    '''
    rules_store.append(p.slice)

def p_ImportDeclarations(p):
    '''
    ImportDeclarations : ImportDeclaration
    | ImportDeclarations ImportDeclaration
    '''
    rules_store.append(p.slice)

def p_TypeDeclarations(p):
    '''
    TypeDeclarations : TypeDeclaration
    | TypeDeclarations TypeDeclaration
    '''
    rules_store.append(p.slice)

def p_PackageDeclaration(p):
    '''
    PackageDeclaration : PACKAGE Name STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_ImportDeclaration(p):
    '''
    ImportDeclaration : SingleTypeImportDeclaration
    | TypeImportOnDemandDeclaration
    '''
    rules_store.append(p.slice)

def p_SingleTypeImportDeclaration(p):
    '''
    SingleTypeImportDeclaration : IMPORT Name STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_TypeImportOnDemandDeclaration(p):
    '''
    TypeImportOnDemandDeclaration : IMPORT Name DOT MULT STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_TypeDeclaration(p):
    '''
    TypeDeclaration : ClassDeclaration
    | STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_Modifiers(p):
    '''
    Modifiers : Modifier
    | Modifiers Modifier
    '''
    rules_store.append(p.slice)

def p_Modifier(p):
    '''
    Modifier : STATIC
    | FINAL
    '''
    rules_store.append(p.slice)
# Section 19.8

def p_ClassDeclaration(p):
    '''
    ClassDeclaration : Modifiers CLASS IDENTIFIER Super ClassBody
    | Modifiers CLASS IDENTIFIER ClassBody
    | CLASS IDENTIFIER Super ClassBody
    | CLASS IDENTIFIER ClassBody
    '''
    rules_store.append(p.slice)

def p_Super(p):
    '''
    Super : EXTENDS ClassType
    '''
    rules_store.append(p.slice)

def p_ClassBody(p):
    '''
    ClassBody : BLOCK_OPENER BLOCK_CLOSER
    | BLOCK_OPENER ClassBodyDeclarations BLOCK_CLOSER
    '''
    rules_store.append(p.slice)

def p_ClassBodyDeclarations(p):
    '''
    ClassBodyDeclarations : ClassBodyDeclaration
    | ClassBodyDeclarations ClassBodyDeclaration
    '''
    rules_store.append(p.slice)

def p_ClassBodyDeclaration(p):
    '''
    ClassBodyDeclaration : ClassMemberDeclaration
    | ConstructorDeclaration
    | StaticInitializer
    '''
    rules_store.append(p.slice)

def p_ClassMemberDeclaration(p):
    '''
    ClassMemberDeclaration : FieldDeclaration
    | MethodDeclaration
    '''
    rules_store.append(p.slice)

def p_FieldDeclaration(p):
    '''
    FieldDeclaration : Modifiers Type VariableDeclarators STMT_TERMINATOR
    | Type VariableDeclarators STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_VariableDeclarators(p):
    '''
    VariableDeclarators : VariableDeclarator
    | VariableDeclarators COMMA VariableDeclarator
    '''
    if(len(p)==2):
        p[0]=p[1]
    else:
        p[0]=p[1]+p[3]

    rules_store.append(p.slice)

def p_VariableDeclarator(p):
    '''
    VariableDeclarator : VariableDeclaratorId
    | VariableDeclaratorId ASSIGN VariableInitializer
    '''
    if(len(p)==2):
        p[0]=p[1]
    elif(type(p[3])!=type({})):
        return
    if( 'isArray' in p[3].keys() and p[3]['isArray']):
        TAC.emit('declare',p[1][0],p[3]['place'],p[3]['type'])
        p[0]=p[1]
    else:
        TAC.emit(p[1][0],p[3]['place'],'',p[2])
        p[0] = p[1]
    rules_store.append(p.slice)

def p_VariableDeclaratorId(p):
    '''
    VariableDeclaratorId : IDENTIFIER
    | VariableDeclaratorId L_SQBR R_SQBR
    '''
    rules_store.append(p.slice)

def p_VariableInitializer(p):
    '''
    VariableInitializer : Expression
    | ArrayInitializer
    '''
    if(len(p)==2):
        p[0]=p[1]
        return
    rules_store.append(p.slice)

def p_MethodDeclaration(p):
    '''
    MethodDeclaration : MethodHeader MethodBody
    '''
    rules_store.append(p.slice)

def p_MethodHeader(p):
    '''
    MethodHeader : Modifiers Type MethodDeclarator Throws
    | Modifiers Type MethodDeclarator
    | Type MethodDeclarator Throws
    | Type MethodDeclarator
    | Modifiers VOID MethodDeclarator Throws
    | Modifiers VOID MethodDeclarator
    | VOID MethodDeclarator Throws
    | VOID MethodDeclarator
    '''
    rules_store.append(p.slice)

def p_MethodDeclarator(p):
    '''
    MethodDeclarator : IDENTIFIER L_PAREN R_PAREN
    | IDENTIFIER L_PAREN FormalParameterList R_PAREN
    '''
    if(len(p)>3):
        label1 = TAC.newLabel()
        TAC.emit('func','','','')
        p[0]=[label1]
        stackbegin.append(p[1])
        stackend.append(l1)
        TAC.emit('label',p[1][0],'','')
    rules_store.append(p.slice)

def p_FormalParametersList(p):
    '''
    FormalParameterList : FormalParameter
    | FormalParameterList COMMA FormalParameter
    '''
    rules_store.append(p.slice)

def p_FormalParameter(p):
    '''
    FormalParameter : Type VariableDeclaratorId
    '''
    rules_store.append(p.slice)

def p_Throws(p):
    '''
    Throws : THROWS ClassTypeList
    '''
    rules_store.append(p.slice)

def p_ClassTypeList(p):
    '''
    ClassTypeList : ClassType
    | ClassTypeList COMMA ClassType
    '''
    rules_store.append(p.slice)

def p_MethodBody(p):
    '''
    MethodBody : Block
    | STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_StaticInitializer(p):
    '''
    StaticInitializer : STATIC Block
    '''
    rules_store.append(p.slice)

def p_ConstructorDeclaration(p):
    '''
    ConstructorDeclaration : Modifiers ConstructorDeclarator Throws ConstructorBody
    | Modifiers ConstructorDeclarator ConstructorBody
    | ConstructorDeclarator Throws ConstructorBody
    | ConstructorDeclarator ConstructorBody
    '''
    rules_store.append(p.slice)

def p_ConstructorDeclarator(p):
    '''
    ConstructorDeclarator : SimpleName L_PAREN FormalParameterList R_PAREN
    | SimpleName L_PAREN R_PAREN
    '''
    rules_store.append(p.slice)

def p_ConstructorBody(p):
    '''
    ConstructorBody : BLOCK_OPENER ExplicitConstructorInvocation BlockStatements BLOCK_CLOSER
    | BLOCK_OPENER ExplicitConstructorInvocation BLOCK_CLOSER
    | BLOCK_OPENER BlockStatements BLOCK_CLOSER
    | BLOCK_OPENER BLOCK_CLOSER
    '''
    rules_store.append(p.slice)

def p_ExplicitConstructorInvocation(p):
    '''
    ExplicitConstructorInvocation : THIS L_PAREN ArgumentList R_PAREN STMT_TERMINATOR
    | THIS L_PAREN R_PAREN STMT_TERMINATOR
    | SUPER L_PAREN ArgumentList R_PAREN STMT_TERMINATOR
    | SUPER L_PAREN R_PAREN STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

# Section 19.9 is about Interfaces

# Section 19.10
def p_ArrayInitializer(p):
    '''
    ArrayInitializer : BLOCK_OPENER VariableInitializers BLOCK_CLOSER
    | BLOCK_OPENER BLOCK_CLOSER
    '''
    rules_store.append(p.slice)

def p_VariableInitializers(p):
    '''
    VariableInitializers : VariableInitializer
    | VariableInitializers COMMA VariableInitializer
    '''
    rules_store.append(p.slice)

# Section 19.11
def p_Block(p):
    '''
    Block : BLOCK_OPENER BLOCK_CLOSER
    | BLOCK_OPENER BlockStatements BLOCK_CLOSER
    '''
    rules_store.append(p.slice)

def p_BlockStatements(p):
    '''
    BlockStatements : BlockStatement
    | BlockStatements BlockStatement
    '''
    rules_store.append(p.slice)

def p_BlockStatement(p):
    '''
    BlockStatement : LocalVariableDeclarationStatement
    | Statement
    '''
    rules_store.append(p.slice)

def p_LocalVariableDeclarationStatement(p):
    '''
    LocalVariableDeclarationStatement : LocalVariableDeclaration STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_LocalVariableDeclaration(p):
    '''
    LocalVariableDeclaration : Type VariableDeclarators
    '''
    for i in p[2]:
        if(p[1]['type']=='SCANNER'):
            p[1]['type']='INT'
                ST.variableAdd(i, i, p[1]['type'])
    rules_store.append(p.slice)

def p_Statement(p):
    '''
    Statement : StatementWithoutTrailingSubstatement
    | LabeledStatement
    | IfThenStatement
    | IfThenElseStatement
    | WhileStatement
    | ForStatement
    '''
    rules_store.append(p.slice)

def p_StatementNoShortIf(p):
    '''
    StatementNoShortIf : StatementWithoutTrailingSubstatement
    | LabeledStatementNoShortIf
    | IfThenElseStatementNoShortIf
    | WhileStatementNoShortIf
    | ForStatementNoShortIf
    '''
    rules_store.append(p.slice)

def p_StatementWithoutTrailingSubstatement(p):
    '''
    StatementWithoutTrailingSubstatement : Block
    | EmptyStatement
    | ExpressionStatement
    | SwitchStatement
    | DoStatement
    | BreakStatement
    | ContinueStatement
    | ReturnStatement
    | ThrowStatement
    | TryStatement
    '''
    rules_store.append(p.slice)

def p_EmptyStatement(p):
    '''
    EmptyStatement : STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_LabeledStatement(p):
    '''
    LabeledStatement : IDENTIFIER COLON Statement
    '''
    rules_store.append(p.slice)

def p_LabeledStatementNoShortIf(p):
    '''
    LabeledStatementNoShortIf : IDENTIFIER COLON StatementNoShortIf
    '''
    rules_store.append(p.slice)

def p_ExpressionStatement(p):
    '''
    ExpressionStatement : StatementExpression STMT_TERMINATOR
    '''
    p[0] = p[1]
    rules_store.append(p.slice)

def p_StatementExpression(p):
    '''
    StatementExpression : Assignment
    | PreIncrementExpression
    | PreDecrementExpression
    | PostIncrementExpression
    | PostDecrementExpression
    | MethodInvocation
    | ClassInstanceCreationExpression
    '''
    rules_store.append(p.slice)

def p_IfThenStatement(p):
    '''
    IfThenStatement : IF L_PAREN Expression R_PAREN Statement
    '''
    rules_store.append(p.slice)

def p_IfThenElseStatement(p):
    '''
    IfThenElseStatement : IF L_PAREN Expression R_PAREN StatementNoShortIf ELSE Statement
    '''
    rules_store.append(p.slice)

def p_IfThenElseStatementNoShortIf(p):
    '''
    IfThenElseStatementNoShortIf : IF L_PAREN Expression R_PAREN StatementNoShortIf ELSE StatementNoShortIf
    '''
    rules_store.append(p.slice)

def p_SwitchStatement(p):
    '''
    SwitchStatement : SWITCH L_PAREN Expression R_PAREN SwitchBlock
    '''
    rules_store.append(p.slice)

def p_SwitchBlock(p):
    '''
    SwitchBlock : BLOCK_OPENER BLOCK_CLOSER
    | BLOCK_OPENER SwitchBlockStatementGroups SwitchLabels BLOCK_CLOSER
    | BLOCK_OPENER SwitchBlockStatementGroups BLOCK_CLOSER
    | BLOCK_OPENER SwitchLabels BLOCK_CLOSER
    '''
    rules_store.append(p.slice)

def p_SwitchBlockStatementGroups(p):
    '''
    SwitchBlockStatementGroups : SwitchBlockStatementGroup
    | SwitchBlockStatementGroups SwitchBlockStatementGroup
    '''
    rules_store.append(p.slice)

def p_SwitchBlockStatementGroup(p):
    '''
    SwitchBlockStatementGroup : SwitchLabels BlockStatements
    '''
    rules_store.append(p.slice)

def p_SwitchLabels(p):
    '''
    SwitchLabels : SwitchLabel
    | SwitchLabels SwitchLabel
    '''
    rules_store.append(p.slice)

def p_SwitchLabel(p):
    '''
    SwitchLabel : CASE ConstantExpression COLON
    | DEFAULT COLON
    '''
    rules_store.append(p.slice)

def p_WhileStatement(p):
    '''
    WhileStatement : WHILE L_PAREN Expression R_PAREN Statement
    '''
    rules_store.append(p.slice)

def p_WhileStatementNoShortIf(p):
    '''
    WhileStatementNoShortIf : WHILE L_PAREN Expression R_PAREN StatementNoShortIf
    '''
    rules_store.append(p.slice)

def p_DoStatement(p):
    '''
    DoStatement : DO Statement WHILE L_PAREN Expression R_PAREN STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_ForStatement(p):
    '''
    ForStatement : FOR L_PAREN ForInit STMT_TERMINATOR Expression STMT_TERMINATOR ForUpdate R_PAREN Statement
    | FOR L_PAREN STMT_TERMINATOR Expression STMT_TERMINATOR ForUpdate R_PAREN Statement
    | FOR L_PAREN ForInit STMT_TERMINATOR STMT_TERMINATOR ForUpdate R_PAREN Statement
    | FOR L_PAREN ForInit STMT_TERMINATOR Expression STMT_TERMINATOR R_PAREN Statement
    | FOR L_PAREN ForInit STMT_TERMINATOR STMT_TERMINATOR R_PAREN Statement
    | FOR L_PAREN STMT_TERMINATOR Expression STMT_TERMINATOR R_PAREN Statement
    | FOR L_PAREN STMT_TERMINATOR STMT_TERMINATOR ForUpdate R_PAREN Statement
    | FOR L_PAREN STMT_TERMINATOR STMT_TERMINATOR R_PAREN Statement
    '''
    rules_store.append(p.slice)

def p_ForStatementNoShortIf(p):
    '''
    ForStatementNoShortIf : FOR L_PAREN ForInit STMT_TERMINATOR Expression STMT_TERMINATOR ForUpdate R_PAREN StatementNoShortIf
    | FOR L_PAREN STMT_TERMINATOR Expression STMT_TERMINATOR ForUpdate R_PAREN StatementNoShortIf
    | FOR L_PAREN ForInit STMT_TERMINATOR STMT_TERMINATOR ForUpdate R_PAREN StatementNoShortIf
    | FOR L_PAREN ForInit STMT_TERMINATOR Expression STMT_TERMINATOR R_PAREN StatementNoShortIf
    | FOR L_PAREN ForInit STMT_TERMINATOR STMT_TERMINATOR R_PAREN StatementNoShortIf
    | FOR L_PAREN STMT_TERMINATOR Expression STMT_TERMINATOR R_PAREN StatementNoShortIf
    | FOR L_PAREN STMT_TERMINATOR STMT_TERMINATOR ForUpdate R_PAREN StatementNoShortIf
    | FOR L_PAREN STMT_TERMINATOR STMT_TERMINATOR R_PAREN StatementNoShortIf
    '''
    rules_store.append(p.slice)

def p_ForInit(p):
    '''
    ForInit : StatementExpressionList
    | LocalVariableDeclaration
    '''
    rules_store.append(p.slice)

def p_ForUpdate(p):
    '''
    ForUpdate : StatementExpressionList
    '''
    rules_store.append(p.slice)

def p_StatementExpressionList(p):
    '''
    StatementExpressionList : StatementExpression
    | StatementExpressionList COMMA StatementExpression
    '''
    rules_store.append(p.slice)

def p_BreakStatement(p):
    '''
    BreakStatement : BREAK IDENTIFIER STMT_TERMINATOR
    | BREAK STMT_TERMINATOR
    '''
    if(len(p)==3 and p[1]=='break'):
        TAC.emit('goto',stackend[-1],'','')
        return
    rules_store.append(p.slice)

def p_ContinueStatement(p):
    '''
    ContinueStatement : CONTINUE IDENTIFIER STMT_TERMINATOR
    | CONTINUE STMT_TERMINATOR
    '''
    if(len(p)==3 and p[1]=='continue'):
        TAC.emit('goto',stackbegin[-1],'','')
        return
    rules_store.append(p.slice)

def p_ReturnStatement(p):
    '''
    ReturnStatement : RETURN Expression STMT_TERMINATOR
    | RETURN STMT_TERMINATOR
    '''
    if(len(p)==3 and p[1]=='return'):
        TAC.emit('ret','','','')
        return
    rules_store.append(p.slice)

def p_ThrowStatement(p):
    '''
    ThrowStatement : THROW Expression STMT_TERMINATOR
    '''
    rules_store.append(p.slice)

def p_TryStatement(p):
    '''
    TryStatement : TRY Block Catches
    | TRY Block Catches Finally
    | TRY Block Finally
    '''
    rules_store.append(p.slice)

def p_Catches(p):
    '''
    Catches : CatchClause
    | Catches CatchClause
    '''
    rules_store.append(p.slice)

def p_CatchClause(p):
    '''
    CatchClause : CATCH L_PAREN FormalParameter R_PAREN Block
    '''
    rules_store.append(p.slice)

def p_Finally(p):
    '''
    Finally : FINALLY Block
    '''
    rules_store.append(p.slice)


# Section 19.12

def p_Primary(p):
    '''
    Primary : PrimaryNoNewArray
    | ArrayCreationExpression
    '''
    rules_store.append(p.slice)

def p_PrimaryNoNewArray(p):
    '''
    PrimaryNoNewArray : Literal
    | THIS
    | L_PAREN Expression R_PAREN
    | ClassInstanceCreationExpression
    | FieldAccess
    | MethodInvocation
    | ArrayAccess
    '''
    rules_store.append(p.slice)

def p_ClassInstanceCreationExpression(p):
    '''
    ClassInstanceCreationExpression : NEW ClassType L_PAREN R_PAREN
    | NEW ClassType L_PAREN ArgumentList R_PAREN
    '''
    rules_store.append(p.slice)

def p_ArgumentList(p):
    '''
    ArgumentList : Expression
    | ArgumentList COMMA Expression
    '''
    rules_store.append(p.slice)

def p_ArrayCreationExpression(p):
    '''
    ArrayCreationExpression : NEW PrimitiveType DimExprs Dims
    | NEW PrimitiveType DimExprs
    | NEW ClassType DimExprs Dims
    | NEW ClassType DimExprs
    '''
     #Doing just 2nd rule i.e 1D array
    if(len(p)==4):
        # TAC.emit('declare',p[2],p[3][1:-1])
        p[0]={
            'type' : p[2].upper(),
            'place'  : p[3]['place'],
            'isarray' : True
        }
    rules_store.append(p.slice)

def p_DimExprs(p):
    '''
    DimExprs : DimExpr
    | DimExprs DimExpr
    '''
    if(len(p)==2):
        p[0]=p[1]
        return
    rules_store.append(p.slice)

def p_DimExpr(p):
    '''
    DimExpr : L_SQBR Expression R_SQBR
    '''
    if(p[2]['type']=='INT'):
        p[0]=p[2]
    else:
        TAC.error("Error : Array declaration requires a size as integer : "+p[2]['place'])
    rules_store.append(p.slice)

def p_Dims(p):
    '''
    Dims : L_SQBR R_SQBR
    | Dims L_SQBR R_SQBR
    '''
    if(len(p)==3):
        p[0]=1
    else:
        p[0]=1+p[1]
    rules_store.append(p.slice)

def p_FieldAccess(p):
    '''
    FieldAccess : Primary DOT IDENTIFIER
    | SUPER DOT IDENTIFIER
    '''
    rules_store.append(p.slice)

def p_MethodInvocation(p):
    '''
    MethodInvocation : Name L_PAREN ArgumentList R_PAREN
    | Name L_PAREN R_PAREN
    | Primary DOT IDENTIFIER L_PAREN ArgumentList R_PAREN
    | Primary DOT IDENTIFIER L_PAREN R_PAREN
    | SUPER DOT IDENTIFIER L_PAREN ArgumentList R_PAREN
    | SUPER DOT IDENTIFIER L_PAREN R_PAREN
    '''
    rules_store.append(p.slice)

def p_ArrayAccess(p):
    '''
    ArrayAccess : Name L_SQBR Expression R_SQBR
    | PrimaryNoNewArray L_SQBR Expression R_SQBR
    '''
    rules_store.append(p.slice)

def p_PostfixExpression(p):
    '''
    PostfixExpression : Primary
    | Name
    | PostIncrementExpression
    | PostDecrementExpression
    '''
    p[0] = p[1]
    rules_store.append(p.slice)

def p_PostIncrementExpression(p):
    '''
    PostIncrementExpression : PostfixExpression INCREMENT
    '''
    if(p[1]['type']=='INT'):
        TAC.emit(p[1]['place'],p[1]['place'],'1','+')
        p[0] = {
            'place' : p[1]['place'],
            'type' : 'INT'
        }
    else:
        TAC.error("Error: increment operator can be used with integers only")
    rules_store.append(p.slice)

def p_PostDecrementExpression(p):
    '''
    PostDecrementExpression : PostfixExpression DECREMENT
    '''
    if(p[1]['type']=='INT'):
        TAC.emit(p[1]['place'],p[1]['place'],'1','-')
        p[0] = {
            'place' : p[1]['place'],
            'type' : 'INT'
        }
    else:
        TAC.error("Error: decrement operator can be used with integers only")
    rules_store.append(p.slice)

def p_UnaryExpression(p):
    '''
    UnaryExpression : PreIncrementExpression
    | PreDecrementExpression
    | PLUS UnaryExpression
    | MINUS UnaryExpression
    | UnaryExpressionNotPlusMinus
    '''
    if(len(p)==2):
        p[0] = p[1]
        return
    rules_store.append(p.slice)

def p_PreIncrementExpression(p):
    '''
    PreIncrementExpression : INCREMENT UnaryExpression
    '''
    if(p[2]['type']=='INT'):
        TAC.emit(p[2]['place'],p[2]['place'],'1','+')
        p[0] = {
            'place' : p[2]['place'],
            'type' : 'INT'
        }
    else:
        TAC.error("Error: increment operator can be used with integers only")

    rules_store.append(p.slice)

def p_PreDecrementExpression(p):
    '''
    PreDecrementExpression : DECREMENT UnaryExpression
    '''
    if(p[2]['type']=='INT'):
        TAC.emit(p[2]['place'],p[2]['place'],'1','-')
        p[0] = {
            'place' : p[2]['place'],
            'type' : 'INT'
        }
    else:
        TAC.error("Error: decrement operator can be used with integers only"
    rules_store.append(p.slice)

def p_UnaryExpressionNotPlusMinus(p):
    '''
    UnaryExpressionNotPlusMinus : PostfixExpression
    | BITWISE_NOT UnaryExpression
    | LOGICAL_NOT UnaryExpression
    | CastExpression
    '''
    if(len(p)==2):
        p[0] = p[1]
    rules_store.append(p.slice)

def p_CastExpression(p):
    '''
    CastExpression : L_PAREN PrimitiveType Dims R_PAREN UnaryExpression
    | L_PAREN PrimitiveType R_PAREN UnaryExpression
    | L_PAREN Expression R_PAREN UnaryExpressionNotPlusMinus
    | L_PAREN Name Dims R_PAREN UnaryExpressionNotPlusMinus
    '''
    rules_store.append(p.slice)

def p_MultiplicativeExpression(p):
    '''
    MultiplicativeExpression : UnaryExpression
    | MultiplicativeExpression MULT UnaryExpression
    | MultiplicativeExpression DIVIDE UnaryExpression
    | MultiplicativeExpression MODULO UnaryExpression
    '''
    if(len(p)==2):
        p[0] = p[1]
        return
    newPlace = ST.getTemp()
    p[0] = {
        'place' : newPlace,
        'type' : 'TYPE_ERROR'
    }
    if p[1]['type']=='TYPE_ERROR' or p[3]['type']=='TYPE_ERROR':
        return
    if p[2] == '*':
        if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
            p[3] =ResolveRHSArray(p[3])
            p[1] =ResolveRHSArray(p[1])
            TAC.emit(newPlace,p[1]['place'],p[3]['place'],p[2])
            p[0]['type'] = 'INT'
        else:
            TAC.error('Error: Type is not compatible'+p[1]['place']+','+p[3]['place']+'.')
    elif p[2] == '/' :
        if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
            p[3] =ResolveRHSArray(p[3])
            p[1] =ResolveRHSArray(p[1])
            TAC.emit(newPlace,p[1]['place'],p[3]['place'],p[2])
            p[0]['type'] = 'INT'
        else:
            TAC.error('Error: Type is not compatible'+p[1]['place']+','+p[3]['place']+'.')
    elif p[2] == '%':
        if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
            p[3] =ResolveRHSArray(p[3])
            p[1] =ResolveRHSArray(p[1])
            TAC.emit(newPlace,p[1]['place'],p[3]['place'],p[2])
            p[0]['type'] = 'INT'
        else:
            TAC.error('Error: Type is not compatible'+p[1]['place']+','+p[3]['place']+'.')
    rules_store.append(p.slice)

def p_AdditiveExpression(p):
    '''
    AdditiveExpression : MultiplicativeExpression
    | AdditiveExpression PLUS MultiplicativeExpression
    | AdditiveExpression MINUS MultiplicativeExpression
    '''
    if(len(p)==2):
        p[0] = p[1]
        return
    newPlace = ST.getTemp()
    p[0] = {
        'place' : newPlace,
        'type' : 'TYPE_ERROR'
    }
    if p[1]['type']=='TYPE_ERROR' or p[3]['type']=='TYPE_ERROR':
        return
    if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
        p[3] =ResolveRHSArray(p[3])
        p[1] =ResolveRHSArray(p[1])
        TAC.emit(newPlace,p[1]['place'],p[3]['place'],p[2])
        p[0]['type'] = 'INT'
    else:
        TAC.error("Error: integer value is needed")
    rules_store.append(p.slice)

def p_ShiftExpression(p):
    '''
    ShiftExpression : AdditiveExpression
    | ShiftExpression L_SHIFT AdditiveExpression
    | ShiftExpression R_SHIFT AdditiveExpression
    '''
    if(len(p)==2):
        p[0] = p[1]
        return
    rules_store.append(p.slice)

def p_RelationalExpression(p):
    '''
    RelationalExpression : ShiftExpression
    | RelationalExpression LST ShiftExpression
    | RelationalExpression GRT ShiftExpression
    | RelationalExpression LEQ ShiftExpression
    | RelationalExpression GEQ ShiftExpression
    | RelationalExpression INSTANCEOF ReferenceType
    '''
    if(len(p)==2):
        p[0] = p[1]
        return
    l1 = TAC.newLabel()
    l2 = TAC.newLabel()
    l3 = TAC.newLabel()
    newPlace = ST.getTemp()
    p[0]={
        'place' : newPlace,
        'type' : 'TYPE_ERROR'
    }
    if p[1]['type']=='TYPE_ERROR' or p[3]['type']=='TYPE_ERROR':
        return
    if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
        if(p[2]=='>'):
            p[3] =ResolveRHSArray(p[3])
            p[1] =ResolveRHSArray(p[1])
            TAC.emit('ifgoto',p[1]['place'],'g '+p[3]['place'],l2)
            TAC.emit('goto',l1,'','')
            TAC.emit('label',l1,'','')
            TAC.emit(newPlace,'0','','=')
            TAC.emit('goto',l3,'','')
            TAC.emit('label',l2,'','')
            TAC.emit(newPlace,'1','','=')
            TAC.emit('label',l3,'','')
            p[0]['type'] = 'INT'
        elif(p[2]=='>='):
            p[3] =ResolveRHSArray(p[3])
            p[1] =ResolveRHSArray(p[1])
            TAC.emit('ifgoto',p[1]['place'],'ge '+p[3]['place'],l2)
            TAC.emit('goto',l1,'','')
            TAC.emit('label',l1,'','')
            TAC.emit(newPlace,'0','','=')
            TAC.emit('goto',l3,'','')
            TAC.emit('label',l2,'','')
            TAC.emit(newPlace,'1','','=')
            TAC.emit('label',l3,'','')
            p[0]['type'] = 'INT'
        elif(p[2]=='<'):
            p[3] =ResolveRHSArray(p[3])
            p[1] =ResolveRHSArray(p[1])
            TAC.emit('ifgoto',p[1]['place'],'l '+p[3]['place'],l2)
            TAC.emit('goto',l1,'','')
            TAC.emit('label',l1,'','')
            TAC.emit(newPlace,'0','','=')
            TAC.emit('goto',l3,'','')
            TAC.emit('label',l2,'','')
            TAC.emit(newPlace,'1','','=')
            TAC.emit('label',l3,'','')
            p[0]['type'] = 'INT'
        elif(p[2]=='<='):
            p[3] =ResolveRHSArray(p[3])
            p[1] =ResolveRHSArray(p[1])
            TAC.emit('ifgoto',p[1]['place'],'le '+p[3]['place'],l2)
            TAC.emit('goto',l1,'','')
            TAC.emit('label',l1,'','')
            TAC.emit(newPlace,'0','','=')
            TAC.emit('goto',l3,'','')
            TAC.emit('label',l2,'','')
            TAC.emit(newPlace,'1','','=')
            TAC.emit('label',l3,'','')
            p[0]['type'] = 'INT'
    else:
        TAC.error('Error: Type is not compatible'+p[1]['place']+','+p[3]['place']+'.')
    rules_store.append(p.slice)

def p_EqualityExpression(p):
    '''
    EqualityExpression : RelationalExpression
    | EqualityExpression EQUALS RelationalExpression
    | EqualityExpression NOT_EQUAL RelationalExpression
    '''
    if(len(p)==2):
        p[0] = p[1]
        return
    l1 = TAC.newLabel()
    l2 = TAC.newLabel()
    l3 = TAC.newLabel()
    newPlace = ST.getTemp()
    p[0]={
        'place' : newPlace,
        'type' : 'TYPE_ERROR'
    }
    if p[1]['type']=='TYPE_ERROR' or p[3]['type']=='TYPE_ERROR':
        return
    if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
        if(p[2][0]=='='):
            p[3] =ResolveRHSArray(p[3])
            p[1] =ResolveRHSArray(p[1])
            TAC.emit('ifgoto',p[1]['place'],'eq '+p[3]['place'],l2)
            TAC.emit('goto',l1,'','')
            TAC.emit('label',l1,'','')
            TAC.emit(newPlace,'0','','=')
            TAC.emit('goto',l3,'','')
            TAC.emit('label',l2,'','')
            TAC.emit(newPlace,'1','','=')
            TAC.emit('label',l3,'','')
            p[0]['type'] = 'INT'
        else:
            p[3] =ResolveRHSArray(p[3])
            p[1] =ResolveRHSArray(p[1])
            TAC.emit('ifgoto',p[1]['place'],'eq '+p[3]['place'],l2)
            TAC.emit('goto',l1,'','')
            TAC.emit('label',l1,'','')
            TAC.emit(newPlace,'1','','=')
            TAC.emit('goto',l3,'','')
            TAC.emit('label',l2,'','')
            TAC.emit(newPlace,'0','','=')
            TAC.emit('label',l3,'','')
            p[0]['type'] = 'INT'
    else:
        TAC.error('Error: Type is not compatible'+p[1]['place']+','+p[3]['place']+'.')
    rules_store.append(p.slice)

def p_AndExpression(p):
    '''
    AndExpression : EqualityExpression
    | AndExpression BITWISE_AND EqualityExpression
    '''
    if(len(p)==2):
        p[0] = p[1]
        return
    newPlace = ST.getTemp()
    p[0] = {
        'place' : newPlace,
        'type' : 'TYPE_ERROR'
    }
    if p[1]['type']=='TYPE_ERROR' or p[3]['type']=='TYPE_ERROR':
        return
    if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
        p[3] =ResolveRHSArray(p[3])
        p[1] =ResolveRHSArray(p[1])
        TAC.emit(newPlace,p[1]['place'],p[3]['place'],'and')
        p[0]['type'] = 'INT'
    else:
        TAC.error('Error: Type is not compatible'+p[1]['place']+','+p[3]['place']+'.')
    rules_store.append(p.slice)

def p_ExclusiveOrExpression(p):
    '''
    ExclusiveOrExpression : AndExpression
    | ExclusiveOrExpression BITWISE_XOR AndExpression
    '''
    if(len(p)==2):
        p[0] = p[1]
        return
    newPlace = ST.getTemp()
    p[0] = {
        'place' : newPlace,
        'type' : 'TYPE_ERROR'
    }
    if p[1]['type']=='TYPE_ERROR' or p[3]['type']=='TYPE_ERROR':
        return
    if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
        p[3] =ResolveRHSArray(p[3])
        p[1] =ResolveRHSArray(p[1])
        TAC.emit(newPlace,p[1]['place'],p[3]['place'],'xor')
        p[0]['type'] = 'INT'
    else:
        TAC.error('Error: Type is not compatible'+p[1]['place']+','+p[3]['place']+'.')
    rules_store.append(p.slice)

def p_InclusiveOrExpression(p):
    '''
    InclusiveOrExpression : ExclusiveOrExpression
    | InclusiveOrExpression BITWISE_OR ExclusiveOrExpression
    '''
    if(len(p)==2):
        p[0] = p[1]
        return
    newPlace = ST.getTemp()
    p[0] = {
        'place' : newPlace,
        'type' : 'TYPE_ERROR'
    }
    if p[1]['type']=='TYPE_ERROR' or p[3]['type']=='TYPE_ERROR':
        return
    if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
        p[3] =ResolveRHSArray(p[3])
        p[1] =ResolveRHSArray(p[1])
        TAC.emit(newPlace,p[1]['place'],p[3]['place'],'or')
        p[0]['type'] = 'INT'
    else:
        TAC.error('Error: Type is not compatible'+p[1]['place']+','+p[3]['place']+'.')
    rules_store.append(p.slice)

def p_ConditionalAndExpression(p):
    '''
    ConditionalAndExpression : InclusiveOrExpression
    | ConditionalAndExpression LOGICAL_AND InclusiveOrExpression
    '''
    if(len(p)==2):
        p[0] = p[1]
        return
    newPlace = ST.getTemp()
    p[0] = {
        'place' : newPlace,
        'type' : 'TYPE_ERROR'
    }
    if p[1]['type']=='TYPE_ERROR' or p[3]['type']=='TYPE_ERROR':
        p[0]=p[1]
        return
    if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
        p[3] =ResolveRHSArray(p[3])
        p[1] =ResolveRHSArray(p[1])
        TAC.emit(newPlace,p[1]['place'],p[3]['place'],'and')
        p[0]['type'] = 'INT'
    else:
        TAC.error('Error: Type is not compatible'+p[1]['place']+','+p[3]['place']+'.')
    rules_store.append(p.slice)

def p_ConditionalOrExpression(p):
    '''
    ConditionalOrExpression : ConditionalAndExpression
    | ConditionalOrExpression LOGICAL_OR ConditionalAndExpression
    '''
    if(len(p)==2):
        p[0] = p[1]
        return
    newPlace = ST.getTemp()
    p[0] = {
        'place' : newPlace,
        'type' : 'TYPE_ERROR'
    }
    if p[1]['type']=='TYPE_ERROR' or p[3]['type']=='TYPE_ERROR':
        return
    if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
        p[3] =ResolveRHSArray(p[3])
        p[1] =ResolveRHSArray(p[1])
        TAC.emit(newPlace,p[1]['place'],p[3]['place'],'or')
        p[0]['type'] = 'INT'
    else:
        TAC.error('Error: Type is not compatible'+p[1]['place']+','+p[3]['place']+'.')
    rules_store.append(p.slice)

def p_ConditionalExpression(p):
    '''
    ConditionalExpression : ConditionalOrExpression
    | ConditionalOrExpression QUESTION Expression COLON ConditionalExpression
    '''
    if(len(p)==2):
        p[0] = p[1]
        return
    rules_store.append(p.slice)

def p_AssignmentExpression(p):  #TODO: Lambda Expression
    '''
    AssignmentExpression : ConditionalExpression
    | Assignment
    | LAMBDA LambdaExpression
    '''
    if(len(p)==2):
        p[0] = p[1]
        return

    if(p[3]=='Scanner'):
        p[0]=p[3]
        return

    if('input' in p[3].keys() and p[3]['input']):
        dst=p[1]['place']
        if( 'isArrayAccess' in p[1].keys() and p[1]['isArrayAccess']):
            dst=p[1]['place'] + "["+p[1]['index_place'] + "]"
        TAC.emit('input',dst,'','')
        p[0] = {}
        return

    if(type(p[3])!=type({})):
        p[0]=p[3]
        return
#    print(p[3])
    if('isarray' in p[3].keys() and p[3]['isarray'] and p[2]=='='):
        TAC.emit('declare',p[1]['place'],p[3]['place'],p[3]['type'])
        return

    newPlace = ST.getTemp()
    p[0] = {
        'place' : newPlace,
        'type' : 'TYPE_ERROR',
        'isarray': False
    }
    # print(p[3])
    if('input' in p[3].keys() and p[3]['input']):
        p[0] = p[3]
        return
    if p[1]['type']=='TYPE_ERROR' or p[3]['type']=='TYPE_ERROR':
        return
    if p[1]['type'] == 'INT' and p[3]['type'] == 'INT' :
        if(p[2][0]=='='):
            # if( 'isArrayAccess' in p[1].keys() and p[1]['isArrayAccess']):
            #     dst1 = ST.getTemp()
            #     TAC.emit(dst1,p[1]['place']+"["+p[1]['index_place']+"]", '','=')
            #     p[1]['place'] =dst1
            #     p[1]['isArrayAccess'] =False
            #     del p[1]['index_place']

            p[3] = ResolveRHSArray(p[3])

            dst = p[1]['place']
            if( 'isArrayAccess' in p[1].keys() and p[1]['isArrayAccess']):
                dst=p[1]['place'] + "["+p[1]['index_place'] + "]"
            TAC.emit(dst,p[3]['place'],'',p[2])
            p[0] = p[1]
            # print(p[0])
        else:
            p[3]=ResolveRHSArray(p[3])
            # print(p[1])
            new1=p[1].copy()
            new = ResolveRHSArray(p[1])
            p[1]=new1.copy()
            # print(p[1])
            dst = p[1]['place']
            if( 'isArrayAccess' in p[1].keys() and p[1]['isArrayAccess']):
                dst=p[1]['place'] + "["+p[1]['index_place'] + "]"
            TAC.emit(newPlace,new['place'],p[3]['place'],p[2][0])
            # print("lok here=====> " +dst)
            TAC.emit(dst,newPlace,'',p[2][1])
        p[0]['type'] = 'INT'
    else:
        TAC.error('Error: Type is not compatible'+p[1]['place']+','+p[3]['place']+'.')
    rules_store.append(p.slice)

def p_Assignment(p):
    '''
    Assignment : LeftHandSide AssignmentOperator AssignmentExpression
    '''
    rules_store.append(p.slice)

def p_LeftHandSide(p):
    '''
    LeftHandSide : Name
    | FieldAccess
    | ArrayAccess
    '''
    rules_store.append(p.slice)

def p_AssignmentOperator(p):
    '''
    AssignmentOperator : ASSIGN
    | MULTEQ
    | DIVEQ
    | MODEQ
    | PLUSEQ
    | MINUSEQ
    | LSHIFTEQ
    | RSHIFTEQ
    '''
    p[0] = p[1]

    rules_store.append(p.slice)
    #To check if I missed something

def p_Expression(p):
    '''
    Expression : AssignmentExpression
    '''
    p[0] = p[1]    
    rules_store.append(p.slice)

def p_LambdaExpression(p):
    '''
    LambdaExpression : L_PAREN FormalParameterList R_PAREN LAMBDA_TOKEN Block
    | L_PAREN R_PAREN LAMBDA_TOKEN Block
    '''
    rules_store.append(p.slice)

def p_ConstantExpression(p):
    '''
    ConstantExpression : Expression
    '''
    p[0] = p[1]
    rules_store.append(p.slice)

def p_error(p):
    if p == None:
        print str(sys.argv[1])+" ::Something is not right at the end"
    else:
        print str(sys.argv[1])+" :: Syntax error in line no " +  str(p.lineno)
    #print("Syntax Error in line %d" %(p.lineno))


def format_print(LHS, RHS, index):
    print("<p>")
    for i in range(len(LHS)):
        if i == index:
            print("<span style='color:red; font-weight:bold'>" + str(LHS[i]) + "</span>")
        else:
            if str(type(LHS[i])) == "<class 'ply.yacc.YaccSymbol'>":
                print(str(LHS[i]), end=" ")
            else:
                print("<span style='color:blue'>" + str(LHS[i].value) + "</span>", end=" ")

    print("&emsp;<span style='color:black; font-weight:bold;'>----></span>&emsp;", end=" ")

    for i in range(len(RHS)):
        if str(type(RHS[i])) == "<class 'ply.yacc.YaccSymbol'>":
            print(str(RHS[i]), end=" ")
        else:
            print("<span style='color:blue'>" + str(RHS[i].value) + "</span>", end=" ")

    print("</p>")


def html_output(rules_store):
    print("<head><title> Parser for JAVA </title></head>")
    print("<body style='padding: 20px'> <h1> Rightmost Derrivation </h1> <hr>")
    LHS = [rules_store[-1][0]]
    RHS = []
    # print the derivation
    for rule in rules_store[::-1]:
        try:
            index = LHS.index(rule[0])
        except ValueError:
            print("Some Error occured")
            return

        # store the derrivation of the current rule
        part_RHS = [symbol for symbol in rule[1:]]
        RHS = RHS[:index] + part_RHS + RHS[index + 1:]
        format_print(LHS, RHS, index)
        LHS = RHS

    print("</body>")


def main():
    tokens = lexer.tokens
    parser = yacc.yacc()
    inputfile = sys.argv[1]
    file_out = inputfile.split('/')[-1].split('.')[0]
    code = open(inputfile, 'r').read()
    code += "\n"
    parser.parse(code, debug=0)
    sys.stdout = open(file_out + ".html", 'w')
    html_output(rules_store)
    # for i in rules_store:
        # print(i)


if __name__ == "__main__":
    main()
    ST = SymbolTable.SymbolTable()
    TAC = ThreeAddressCode.ThreeAddressCode()

    s = open(sys.argv[1],'r')
    data = s.read()
    data+= "\n"
    s.close()

    #Parse it!
    yacc.parse(data)
    # TAC.output()
    TAC.output3AC()

