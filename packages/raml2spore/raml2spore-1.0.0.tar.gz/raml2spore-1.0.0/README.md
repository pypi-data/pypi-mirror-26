# raml2spore
convert RAML specs to SPORE


## Installation
pip3 install raml2spore

## Usage
raml2spore has a very east interface

for instance you have the following `todoapp.raml` specs
```yaml
#%RAML 1.0

baseUri: http://localhost:5000/api/v1

title: TODO API

types:
    Todo:
        properties:
            id: integer
            title: string
            done: boolean
        example:
            id: 1
            title: "Example todo"
            done: false

/todos:
    get:
        displayName: ListTodos
        description: list all todos
        responses:
            200:
                body:
                    application/json:
                        type: Todo[]
    post:
        displayName: CreateTodo
        description: Create new todo
        body:
            application/json:
                properties:
                    title:
                        type: string
                        required: true
                    done:
                        type: boolean
                        required: true
        responses:
            200:
                body:
                    application/json:
                        type: Todo
    /{id}:
        uriParameters:
            id:
                type: string
        get:
            displayName: GetTodo
            description: Get todo
            responses:
                200:
                    body:
                        application/json:
                            type: Todo[]
        
        patch:
            displayName: UpdateTodo
            description: update todo
            body:
                application/json:
                    properties:
                        title:
                            type: string
                            required: true
                        done:
                            type: boolean
                            required: true
            responses:
                200:
                    body:
                        application/json:
                            type: Todo

```
You can convert it like this
```python

import raml2spore

ramlfile = "todoapp.raml"

spore_file = raml2spore.spore_from_raml_file(ramlfile)
with open("todoapi.json", "w") as f:
    f.write(str(spore_file))
```
It will generate something similiar to this
```
{
    "base_url": "http://localhost:5000/api/v1",
    "meta": {
        "documentation": ""
    },
    "methods": {
        "CreateTodo": {
            "description": "Create new todo",
            "documentation": "Create new todo",
            "expected_status": [
                200
            ],
            "method": "POST",
            "name": "CreateTodo",
            "path": "/todos",
            "required_payload": [
                "title",
                "done"
            ]
        },
        "GetTodo": {
            "description": "Get todo",
            "documentation": "Get todo",
            "expected_status": [
                200
            ],
            "method": "GET",
            "name": "GetTodo",
            "optional_params": [
                "pages"
            ],
            "path": "/todos/:id",
            "required_params": [
                "id"
            ]
        },
        "ListTodos": {
            "description": "list all todos",
            "documentation": "list all todos",
            "expected_status": [
                200
            ],
            "method": "GET",
            "name": "ListTodos",
            "path": "/todos"
        },
        "UpdateTodo": {
            "description": "update todo",
            "documentation": "update todo",
            "expected_status": [
                200
            ],
            "method": "PATCH",
            "name": "UpdateTodo",
            "path": "/todos/:id",
            "required_params": [
                "id"
            ],
            "required_payload": [
                "title",
                "done"
            ]
        }
    }
}
```

Then easily from any language that provides a SPORE client

```lua

-- package.loaded['socket'] = nil

local pretty = require 'pl.pretty'
local function slurp(path)
    print(path)
    local f = io.open(path)
    local s = f:read("*a")
    f:close()
    return s
end
local Spore = require 'Spore'

local defs = slurp("todoapi.json")
local todo = Spore.new_from_string(defs)

todo:enable 'Format.JSON'
pretty.dump(todo)

local res = todo:ListTodos()
pretty.dump(res)

local res = todo:UpdateTodo{id=1, payload={title="oufff!", done=false}}
pretty.dump(res.body)


local res = todo:GetTodo({id=1})
if res.status == 200 then   
    pretty.dump(res.body)
end

```

