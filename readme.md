# JSON Templating

## Stage 1

Write a cli tool using any language you like to resolve JSON templating. 

The usage of the tool is:

`$ jsont input.json params.json`

The json string template syntax is: {{variableName}}. The replace only happens in JSON string values. The left braces can be escaped by {{lb}}. The right braces do not need to be escaped. "lb" cannot be used as a variable name. Variable name can only be \w+. The application writes the result to stdout.

### Stage 1 detailed requirements
	•	You can use the programming language you like.
	•	You can use the existing library to parse JSON.
	•	You can use regex lib.
	•	You cannot use existing templating library.
	•	CLI usage: jsont <input.json> <params.json>, if wrong, print usage and exit code = 1.
	•	If the program cannot read input.json or params.json, or they are invalid json, exit with code = 2, print error to stderr
	•	params.json cannot contain nested structure, object values must all be string type. Object keys should be \w+. If not valid, exit with code = 3.
	•	Var name cannot be lb in params.json, if detected, exit with code = 3.
	•	The variables in params.json should not be replaced/transformed. They are all pure string literals.
	•	Only string value in input.json should be replaced, object key should not be processed. String values in JSON array should be processed, too.
	•	Only one pass of replacement should happen. For example: var1='value1', then {{lb}}{{lb}}var1}} should be {{var1}}; Similarly, given var1='var2', var2='value2', {{{{var1}}}} should be {{var2}}; given var1='}}', {{lb{{var1}} should be {{lb}}
	•	If unknown var name is found in input.json, like {{unknown}}, then you should leave it unchanged.
	•	Print the output to stdout, with indentation = 2 spaces.
	•	Write test cases to verify your implementation.

## Example for Stage 1

input.json:
```
{
    "key1": "some {{var1}}",
    "key2": {
        "{{var1}}": "{{var3}} {{var4}} {{var5}}"
        },
        "key3": [
            "{{var2}} abc",
            "escaped braces: {{lb}}{{lb}}var3}}"
        ]
}
```

params.json:
```
{
    "var1": "value1 {{var2}}",
    "var2": "value2 {{lb}}{{lb}}var3}}",
    "var3": "value3",
    "var4": "value4",
    "var5": "value5"
}
```
Then the output should be:
```
{
    "key1": "some value1 {{var2}}",
    "key2": {
        "{{var1}}": "value3 value4 value5"
        },
        "key3": [
            "value2 {{lb}}{{lb}}var3}} abc",
            "escaped braces: {{var3}}"
        ]
}
```

## Stage 2

If you finish stage 1 and still have extra time, please consider implementing stage 2, the recursive param mode.
Add a switch -r to enable the recursive mode.
## Stage 2 detailed requirements
	•	The variable values now can reference other variables, recursively.
	•	If there are circular references, exit with code = 4.
	•	{{lb}} should be escaped to { in params.json.
	•	{{unknown}} in variable values should not be processed.
	•	Given var1='{{lb{{var2}}', var2='}}', var1's final value should be {{lb}}
	•	Given var1='{{lb}}{{lb}}var2}}', var1's final value should be {{var2}}


## Example for Stage 2


input.json:
```
{
    "key1": "{{var1}} {{var2}} {{var3}}",
    "key2": {
        "{{var2}}": "{{var4}}"
        },
        "{{var3}}": [
            "{{var5}} {{var6}}"
            ]
}
```
params.json:
```
{
    "var1": "{{var2}}",
    "var2": "{{var3}}",
    "var3": "3",
    "var4": "4 -> {{var3}}",
    "var5": "{{varNONO}}"
}
```
output:
```
{
    "key1": "3 3 3",
    "key2": {
        "{{var2}}": "4 -> 3"
        },
        "{{var3}}": [
            "{{varNONO}} {{var6}}"
            ]
}
```

