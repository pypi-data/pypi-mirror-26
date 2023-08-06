# password-generator:
Generates a memorable (by pattern), strong (long and mixed characters) passwords.

# Install
`pip install password_gen`

# Documentation
`generate(pattern, dictionary, digits, characters)`: Generates password


>`pattern:{string: d - number, wi - word of length i, s - any special character} specify pattern of the password. Ex 'w3-d.w5!' -> cat-1.horse!`


>`dictionary:{list} a list of preferred words`


>`digits:{list} a list specifying the range of digits. Ex [2, 8] -> digits from 2 to 7`


>`characters:{list} a list specifying the range of ascii values of special characters. Ex [33, 36] -> '!, ~, #, $'`

# Usage
``` python
import password_gen as pg

print( pg.generate() )

#  with all parameters
print( pg.generate('w5-dd-w3.d',['willy', 'wonka', 'and', 'the', 'chocolate', 'factory'], [3, 8], [35, 38]))
# -> "Wonka-55-the.6"

# with some parameter
print( pg.generate('d.w4.d.w5!') )
# -> "2.PrAy.0.Filed!"

print( pg.generate(dictionary=['willy', 'wonka', 'and', 'the', 'chocolate', 'factory']) )
# -> "6wOnkA(and,ChocolatE&willy4"

print( pg.generate(digits=[2,5], characters=[33, 35]) )
# -> "#outsourcing4frequent5wArehoUse3sTreaM#"
```
