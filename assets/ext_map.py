from .._pieces_lib.pieces_os_client import ClassificationSpecificEnum

class SyntaxFileMap(dict):
    """
        Class for caching the reverse keys of the map
        It maps all the extensions to their syntax
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SyntaxFileMap, cls).__new__(cls)
            cls._instance.__init__(*args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            super().__init__(
                {
                    ClassificationSpecificEnum.BAT: 'Packages/Batch File/Batch File.sublime-syntax',
                    ClassificationSpecificEnum.C: 'Packages/C++/C.sublime-syntax',
                    ClassificationSpecificEnum.CS: 'Packages/C#/C#.sublime-syntax',
                    ClassificationSpecificEnum.CPP: 'Packages/C++/C++.sublime-syntax',
                    ClassificationSpecificEnum.CSS: 'Packages/CSS/CSS.sublime-syntax',
                    ClassificationSpecificEnum.ERL: 'Packages/Erlang/Erlang.sublime-syntax',
                    ClassificationSpecificEnum.GO: 'Packages/Go/Go.sublime-syntax',
                    ClassificationSpecificEnum.HS: 'Packages/Haskell/Haskell.sublime-syntax',
                    ClassificationSpecificEnum.HTML: 'Packages/HTML/HTML.sublime-syntax',
                    ClassificationSpecificEnum.JAVA: 'Packages/Java/Java.sublime-syntax',
                    ClassificationSpecificEnum.JS: 'Packages/JavaScript/JavaScript.sublime-syntax',
                    ClassificationSpecificEnum.TSX: 'Packages/JavaScript/TSX.sublime-syntax',
                    ClassificationSpecificEnum.JSX: 'Packages/JavaScript/JSX.sublime-syntax',
                    ClassificationSpecificEnum.LUA: 'Packages/Lua/Lua.sublime-syntax',
                    ClassificationSpecificEnum.PHP: 'Packages/PHP/PHP.sublime-syntax',
                    ClassificationSpecificEnum.PY: 'Packages/Python/Python.sublime-syntax',
                    ClassificationSpecificEnum.PL: 'Packages/Perl/Perl.sublime-syntax',
                    ClassificationSpecificEnum.MD: 'Packages/Markdown/Markdown.sublime-syntax',
                    ClassificationSpecificEnum.MATLAB: 'Packages/Matlab/Matlab.sublime-syntax',
                    ClassificationSpecificEnum.M: 'Packages/Objective-C/Objective-C.sublime-syntax',
                    ClassificationSpecificEnum.R: 'Packages/R/R.sublime-syntax',
                    ClassificationSpecificEnum.RB: 'Packages/Ruby/Ruby.sublime-syntax',
                    ClassificationSpecificEnum.RS: 'Packages/Rust/Rust.sublime-syntax',
                    ClassificationSpecificEnum.SCALA: 'Packages/Scala/Scala.sublime-syntax',
                    ClassificationSpecificEnum.BASH: 'Packages/ShellScript/Bash.sublime-syntax',
                    ClassificationSpecificEnum.SQL: 'Packages/SQL/SQL.sublime-syntax',
                    ClassificationSpecificEnum.TS: 'Packages/JavaScript/TypeScript.sublime-syntax',
                    ClassificationSpecificEnum.JSON: 'Packages/JSON/JSON.sublime-syntax',
                    ClassificationSpecificEnum.YML: 'Packages/YAML/YAML.sublime-syntax',
                    ClassificationSpecificEnum.YAML: 'Packages/YAML/YAML.sublime-syntax',
                    ClassificationSpecificEnum.GROOVY: 'Packages/Groovy/Groovy.sublime-syntax',
                    ClassificationSpecificEnum.XML: 'Packages/XML/XML.sublime-syntax'
                }
            )
            self._reverse = {v: k for k, v in self.items()}

            self.initialized = True

    @property
    def reverse(self):
        return self._reverse
    

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._reverse[value] = key

    def __delitem__(self, key):
        value = self[key]
        super().__delitem__(key)
        del self._reverse[value]

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        
        # Update the reverse dictionary
        for key, value in dict(*args, **kwargs).items():
            self._reverse[value] = key

file_map = SyntaxFileMap()


