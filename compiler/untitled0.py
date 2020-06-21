__PROG__ -> __WORD__ ( ) __BLOCK__

__DECLS__ -> __DECLS__ __DECL__
__DECLS__ -> ''

__DECL__ -> __VTYPE__ __WORDS__ ;


__WORDS__ -> __WORDS__ , __WORD__
__WORDS__ -> __WORD__

__VTYPE__ -> int
__VTYPE__ -> char

__BLOCK__ -> { __DECLS__ __SLIST__ }
__BLOCK__ -> ''

__SLIST__ -> __SLIST__ __STAT__
__SLIST__ -> __STAT__

__STAT__ -> IF __COND__  THEN __BLOCK__ ELSE __BLOCK__
__STAT__ -> WHILE __COND__ __BLOCK__
__STAT__ -> __WORD__ = __EXPR__ ; 
__STAT__ -> RETURN __EXPR__ ;

__COND__ -> __EXPR__ > __EXPR__
__COND__ -> __EXPR__ == __EXPR__

__EXPR__ -> __TERM__
__EXPR__ -> __TERM__ + __TERM__

__TERM__ -> __FACT__
__TERM__ -> __FACT__ * __FACT

__FACT__ -> __NUM__
__FACT__ -> __WORD__


