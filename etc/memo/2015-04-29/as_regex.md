# policy condition

## aspath condition

#### cisco AS regex
```
Cisco AS regex

Range
A range is a sequence of characters within left and right square brackets. An example is [abcd].
Atom
An atom is a single character. Here are some examples:
.	The . matches any single character.
^	The ^ matches the start of the input string.
$	The $ matches the end of the input string.
\	The \ matches the character.
-	The _ matches a comma (,), left brace ({), right brace (}), the start of the input string, the end of the input string, or a space.

Piece
A piece is one of these symbols, which follows an atom:
*	The * matches 0 or more sequences of the atom.
+	The + matches 1 or more sequences of the atom.
?	The ? matches the atom or the null string.

Branch
A branch is 0 or more concatenated pieces.
Here are some examples of regular expressions:
a*	This expression indicates any occurrence of the letter "a", which includes none.
a+	This expression indicates that at least one occurrence of the letter "a" must be present.
ab?a	This expression matches "aa" or "aba".

_100_	This expression means via AS100.
_100$	This expression indicates an origin of AS100.
^100 .*	This expression indicates transmission from AS100.
^$	This expression indicates origination from this AS.
```

#### AS PATH condition

- \_100_


