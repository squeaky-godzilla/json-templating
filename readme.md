# JSON Templating

Simple cli tool to resolve JSON templating. 

The usage of the tool is:

`$ jsont input.json params.json`

The json string template syntax is: {{variableName}}. The replace only happens in JSON string values. The left braces can be escaped by {{lb}}. The right braces do not need to be escaped. "lb" cannot be used as a variable name. Variable name can only be \w+. The application writes the result to stdout.

## Example

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
Then the output will be:
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

## Recursive mode

Add a switch -r to enable the recursive mode.

## Example for recursive mode


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

