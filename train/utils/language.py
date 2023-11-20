from enum import Enum


class Language(Enum):
    OTHER = 0
    C = 1
    CPLUSPLUS = 2
    CSHARP = 3
    CSS = 4
    DART = 5
    DOCKER = 6
    FUNC = 7
    GO = 8
    HTML = 9
    JAVA = 10
    JAVASCRIPT = 11
    JSON = 12
    KOTLIN = 13
    LUA = 14
    NGINX = 15
    OBJECTIVE_C = 16
    PHP = 17
    POWERSHELL = 18
    PYTHON = 19
    RUBY = 20
    RUST = 21
    SHELL = 22
    SOLIDITY = 23
    SQL = 24
    SWIFT = 25
    TL = 26
    TYPESCRIPT = 27
    XML = 28


ROSETTA_CODE_TO_LANGUAGE = {
    'C': Language.C,
    'C++': Language.CPLUSPLUS,
    'C-sharp': Language.CSHARP,
    'Dart': Language.DART,
    'Go': Language.GO,
    'Java': Language.JAVA,
    'JavaScript': Language.JAVASCRIPT,
    'JSON': Language.JSON,
    'Kotlin': Language.KOTLIN,
    'Lua': Language.LUA,
    'Objective-C': Language.OBJECTIVE_C,
    'PHP': Language.PHP,
    'PowerShell': Language.POWERSHELL,
    'Python': Language.PYTHON,
    'Ruby': Language.RUBY,
    'Rust': Language.RUST,
    'UNIX-Shell': Language.SHELL,
    'SQL': Language.SQL,
    'Swift': Language.SWIFT,
    'TypeScript': Language.TYPESCRIPT
}
