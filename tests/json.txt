*** Setting ***

Library  HttpLibrary.HTTP
Library  Collections

*** Test Cases ***

Should Be Valid Json OK
    Should Be Valid JSON  {"foo": "bar"}

Should Be Valid Json FAIL
    ${python_ver}=   Get Major Python Version
    Run Keyword If  '${python_ver}' == '3'
    ...           Run Keyword And Expect Error
    ...               ValueError: Could not parse '-oh 748903' as JSON: Expecting value: line 1 column 1 (char 0)
    ...               Should Be Valid JSON  -oh 748903
    ...           ELSE
    ...           Run Keyword And Expect Error
    ...               ValueError: Could not parse '-oh 748903' as JSON: No JSON object could be decoded
    ...               Should Be Valid JSON  -oh 748903

Get Json Value OK
    Set Test Variable  ${obj}          {"foo":{"another prop":{"baz":"A string"}}}
    ${result}=         Get Json Value  ${obj}       /foo/another prop/baz
    Should Be Equal    ${result}       "A string"

Get Json Value Fail
    Set Test Variable  ${obj}          {"foo":{"another prop":{"baz":"A string"}}}
    ${python_ver}=    Get Major Python Version
    Run Keyword If  '${python_ver}' == '3'
    ...           Run Keyword And Expect Error
    ...               EQUALS: JsonPointerException: member 'bar' not found in {'baz': 'A string'}
    ...               Get Json Value  ${obj}       /foo/another prop/bar
    ...           ELSE
    ...           Run Keyword And Expect Error
    ...               EQUALS: JsonPointerException: member 'bar' not found in {u'baz': u'A string'}
    ...               Get Json Value  ${obj}       /foo/another prop/bar

Get Json Value Documentation
    ${result}=       Get Json Value  {"foo": {"bar": [1,2,3]}}  /foo/bar
    Should Be Equal  ${result}       [1, 2, 3]

Parse Json True
    ${result}=       Parse Json      true
    Should Be True   ${result}

Parse Json Null
    ${result}=                  Parse Json      null
    Should Be Equal As Strings  ${result}       None

Parse Json Array
    ${result}=        Parse Json      [1,2,3,4,5,6,7,8,9,10]
    Length Should Be  ${result}       10

Set Json Value
    Set Test Variable  ${obj}          {"foo":"bar"}
    ${result}=         Set Json Value  ${obj}          /baz   9
    Should Be True    '${result}'=='{"foo": "bar", "baz": 9}' or '${result}'=='{"baz": 9, "foo": "bar"}'

Set Complex Json Value
    Set Test Variable  ${obj}          {}
    ${result}=         Set Json Value  ${obj}          /baz   ["12", "13", [{"bar": "biz"}]]
    Should Be Equal    ${result}       {"baz": ["12", "13", [{"bar": "biz"}]]}

Set Json Value Documentation
    ${result}=       Set Json Value  {"foo": {"bar": [1,2,3]}}  /foo  12
    Should Be Equal  ${result}       {"foo": 12}

Create Large JSON Document
    ${document}=  Catenate
    ...  {
    ...  "name" : "jsonpointer",
    ...  "description" : "Simple JSON Addressing.",
    ...  "tags" : ["util", "simple", "util", "utility"],
    ...  "version" : "1.0.1",
    ...  "author" : "Jan Lehnardt <jan@apache.org>",
    ...  "repository" :
    ...  {
    ...    "type" : "git",
    ...    "url" : "http://github.com/janl/node-jsonpointer.git"
    ...  },
    ...  "bugs" :
    ...  { "web" : "http://github.com/janl/node-jsonpointer/issues" },
    ...  "engines" : ["node >= 0.4.9"],
    ...  "main" : "./jsonpointer",
    ...  "scripts" : { "test" : "node test.js" }
    ...  }
    Should Be Valid JSON    ${document}
    ${result}=       Get Json Value  ${document}  /repository/type
    Should Be Equal  ${result}       "git"

Json Value Should Be OK
    Set Test Variable        ${doc}  {"foo": {"bar": [1,2,3]}}
    Json Value Should Equal  ${doc}  /foo/bar                   [1, 2, 3]

Json Value Should Not Be OK
    Set Test Variable            ${doc}  {"foo": {"bar": [1,2,3]}}
    Json Value Should Not Equal  ${doc}  /foo/bar                   [4, 9, 18]

Json Value Should Be Fail
    Set Test Variable        ${doc}  {"foo": {"bar": [4,5,6]}}
    Run Keyword And Expect Error
    ...  EQUALS: JSON value "[4, 5, 6]" does not equal "[1, 2, 3]", but should have.
    ...  Json Value Should Equal  ${doc}  /foo/bar  [1, 2, 3]

Json Value Should Be Fail Invalid Pointer
    Set Test Variable        ${doc}  {"foo": {"bar": [4,5,6]}}
    ${python_ver}=   Get Major Python Version
    Run Keyword If  '${python_ver}' == '3'
    ...           Run Keyword And Expect Error
    ...               EQUALS: JsonPointerException: member 'baz' not found in {'foo': {'bar': [4, 5, 6]}}
    ...               Json Value Should Equal  ${doc}  /baz  [7,8,9]
    ...           ELSE
    ...           Run Keyword And Expect Error
    ...               EQUALS: JsonPointerException: member 'baz' not found in {u'foo': {u'bar': [4, 5, 6]}}
    ...               Json Value Should Equal  ${doc}  /baz  [7,8,9]

Stringify Documentation Example
    ${data} =                   Create List      1  2  3
    ${json_string}=             Stringify JSON   ${data}
    Should Be Equal As Strings  ${json_string}   ["1", "2", "3"]

Stringify Complex Object
    ${names} =       Create List         First Name     Family Name    Email
    ${data} =        Create Dictionary   names  ${names}   a  1   b  12
    ${json_string}=  Stringify JSON      ${data}

    Should Be Equal As Strings  ${json_string}   {"names": ["First Name", "Family Name", "Email"], "a": "1", "b": "12"}

Stringify Data With Chinese String
    Set Test Variable  ${data}  中
    ${json_string}=             Stringify JSON   ${data}
    Should Be Equal As Strings  ${json_string}   "${data}"

Get Json Value In Chinese OK
    Set Test Variable  ${chinese}       "中"
    ${result}=  Get Json Value  {"foo":${chinese}}   /foo
    Should Be Equal    ${result}       ${chinese}
