## Stem - Backend App Controller 
Libraries behind ASGI server.

Entities and functions can be shared across different projects

## Request flow
Server -- Stem -- Business logic
```
Stem
├── protocol      # abstract entities
├── core          # core entities
│   ├── config        # 数据访问对象
│   ├── controller    # 数据访问对象
│   ├── service       # 数据访问对象
│   └── handler       # 数据访问对象
├── loader        # connect request and logic code
│   ├── connector # connect controller
│   └── loader    # load codes
├── db            # 数据模型相关代码
│   ├── dao       # 数据访问对象
│   └── model     # API对象
└── readme.md
```