import os
import re
import subprocess

from module import Path
from PyQt5.QtCore import QThread, pyqtSignal

from .specfile import SpecFile

path = Path(__file__)


class CompileInThread(QThread):
    output = pyqtSignal(str)
    end = pyqtSignal(str)

    def __init__(self, parent=None, code: str = "", file_code: str = ""):
        super().__init__(parent)
        self._compile = Compile(code, file_code)

    def run(self):
        end_out = ""
        for out in self._compile.run():
            self.output.emit(out)
            end_out = out
        self.end.emit(re.sub(r"Error,\s", "", end_out))

    def stop(self):
        self.terminate()
        if self._compile.pid is not None:
            os.system(f"taskkill /f /pid {self._compile.pid}")
        return self._compile.pid


class Compile:

    @staticmethod
    def __not_found_other_cmd(lines: list, idx: int):
        return idx + 1 < len(lines) and not re.search(r"\[.+?]", lines[idx+1])

    @staticmethod
    def __remake_path(_path):
        return re.sub(r"\\", r"\\\\", os.path.normpath(_path))

    @staticmethod
    def __subprocess_args(include_stdout=True):
        if hasattr(subprocess, 'STARTUPINFO'):
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            env = os.environ
        else:
            si = None
            env = None
        if include_stdout:
            ret = {'stdout': subprocess.PIPE}
        else:
            ret = {}
        ret.update({'stdin': subprocess.PIPE,
                    'stderr': subprocess.PIPE,
                    'startupinfo': si,
                    'env': env})
        return ret

    def __init__(self, code: str, file_code: str):
        self.file_code = file_code
        self.pid = None
        self.converter = "pyinstaller"
        self.input_file = ""
        self.output_dir = ""
        self.name = ""
        self.pathex = []
        self.data = []
        self.binaries = []
        self.hidden_imports = []
        self.icon = ""
        self.console = True
        self.one_file = False
        self.uac_admin = False
        self.code = re.sub(r"\*ThisDir\*", re.escape(os.path.dirname(self.file_code)), code)
        self.code_lines = self.code.split("\n")

    def __get_code_blocks(self, *blocks):

        def is_block_name(line):
            for block in blocks:
                if f"[{block}]" == line:
                    return True
            return False

        b = []
        line = 1
        i = 0
        end = len(self.code_lines)
        while i < end:
            block_name = ""
            code_line = self.code_lines[i]
            if is_block_name(code_line):
                block_name = code_line
                line = i + 1
            i += 1
            if not block_name:
                continue
            block_code = []
            while i < end and not is_block_name(self.code_lines[i]):
                if self.code_lines[i].strip() and not re.search("^#", self.code_lines[i].lstrip()):
                    block_code.append({"line": i + 1, "code": self.code_lines[i].lstrip()})
                i += 1
            b.append(Compile.CodeBlock(line, block_name, block_code))
        return b

    class CodeBlock(object):
        def __init__(self, line, block_name, code_block):
            self.name = block_name[1:-1]
            self.block_name = block_name
            self.list_dict = code_block
            self.code = "\n".join([c["code"] for c in self.list_dict])
            self.lines_n_code = [(c['line'], c['code']) for c in self.list_dict]
            self.line = line

        def __str__(self):
            return f"line: {self.line} {self.block_name}\n" + "\n".join([f"line: {c['line']} {c['code']}" for c in self.list_dict])

        def get_variables(self, *variable):
            var = []
            for i, l in self.lines_n_code:
                for v in variable:
                    f = re.search(rf"{v}\s*=.+", l)
                    if f:
                        var.append(Compile.Variable(v, f.group().split("=")[1].lstrip(), i))
                        break
                else:
                    if re.search(r".+", l):
                        var.append(Compile.InvalidVariable(l, i))
            return var

        def get_sources(self):
            sources = []
            for i, l in self.lines_n_code:
                f = re.search(r"Source\s.+\sDestDir\s.+|Source\s.+", l)
                if f:
                    f = f.group()
                    if " DestDir " in f:
                        d = f.split(" DestDir ")
                        sources.append(Compile.SourceVariable(d[0][7:], d[1], i))
                    else:
                        sources.append(Compile.SourceVariable(f[7:], None, i))
                else:
                    sources.append(Compile.InvalidVariable(l, i))
            return sources

        def get_lines_valid(self, *valid):
            var = []
            for i, l in self.lines_n_code:
                if l.strip() in valid:
                    var.append(Compile.LineValid(l, i))
                else:
                    var.append(Compile.InvalidVariable(l, i))
            return var


    class LineValid(object):
        def __init__(self, value, line):
            self.value = value
            self.line = line

        def __str__(self) -> str:
            return f"Line {self.line}: {self.value}"

    class InvalidVariable(object):
        def __init__(self, value, line):
            self.value = value
            self.line = line
            self.valid = False

        def __str__(self) -> str:
            return f"Line {self.line}: Invalid Variable"


    class Variable(object):
        def __init__(self, name, value, line):
            self.name = name
            self.value = value
            self.line = line

        def __str__(self) -> str:
            return f"Line {self.line}: {self.name} = {self.value}"

    class SourceVariable(object):
        def __init__(self, value, dest_dir, line):
            self.path = Compile.Path(value)
            self.valid = not self.path.error
            self.dest_dir = dest_dir
            self.line = line

        def __str__(self):
            return f"Line {self.line}: {self.path.value}, {self.dest_dir}"

    class FileName(object):
        def __init__(self, value):
            r = re.search(r'(?<=").+(?=")', value)
            self.value = r.group() if r else ""
            self.valid = not re.search(r'[\/:*?"<>|]', self.value)

        def __str__(self):
            return self.value

    class Path(object):
        def __init__(self, value):
            self.value = os.path.normpath(value)
            if not os.path.exists(value):
                self.error = f"No such file or directory {self.value}"
            else:
                self.error = ""
            self.isfile = os.path.isfile(self.value)
            self.isdir = os.path.isdir(self.value)

    def block_setup(self, code_block):
        self.converter = "pyinstaller"
        self.input_file = ""
        self.output_dir = ""
        self.icon = ""
        self.name = ""
        for variable in code_block.get_variables("Converter", "InputFile", "OutputDir", "Icon", "AppName"):
            if isinstance(variable, Compile.InvalidVariable):
                return f"Error, line {variable.line}, Invalid variable"
            if variable.name == "AppName":
                name = Compile.FileName(variable.value)
                if not name.value:
                    return f"Error, line {variable.line}, File name must not be empty"
                if not name.valid:
                    return f"Error, line {variable.line}, A file name can't contain any of the following characters: \\ / : * ? \" < > |"
                self.name = name.value
            if variable.name == "Converter":
                if variable.value != "PyInstaller":
                    p = os.path.normpath(variable.value)
                    if os.path.isfile(p):
                        self.converter = self.__remake_path(p)
                    else:
                        return f"Error, line {variable.line}, Converter variable invalid"
            elif variable.name == "InputFile":
                p = os.path.normpath(variable.value)
                if os.path.isfile(p):
                    t = os.path.splitext(os.path.basename(p))[1]
                    if t == ".py" or t == ".pyw":
                        self.input_file = self.__remake_path(p)
                    else:
                        return f"Error, line {variable.line}, Input file must be python file"
                else:
                    return f"Error, line {variable.line}, No such file \"{p}\""
            elif variable.name == "OutputDir":
                p = os.path.normpath(variable.value)
                if os.path.isdir(p):
                    self.output_dir = self.__remake_path(p)
                else:
                    return f"Error, line {variable.line}, No such file \"{p}\""
            elif variable.name == "Icon":
                if variable.value == "NONE":
                    self.icon = "NONE"
                elif variable.value == "Default":
                    self.icon = ""
                else:
                    p = os.path.normpath(variable.value)
                    if os.path.isfile(p):
                        if os.path.splitext(os.path.basename(p))[1] != ".ico":
                            return f"Error, line {variable.line}, Icon file type is not supported (.ico only)"
                        self.icon = self.__remake_path(p)
                    else:
                        return f"Error, line {variable.line}, Icon file \"{p}\" invalid (must be NONE, Default or path to file .ico)"
        if not self.input_file:
            return f"Error, InputFile not found in [Setup]"
        if not self.output_dir:
            self.output_dir = os.path.dirname(self.file_code)
        if not self.name:
            self.name = os.path.splitext(os.path.basename(self.input_file))[0]

    def block_option(self, block_code):
        self.one_file = False
        self.console = True
        self.uac_admin = False
        for variable in block_code.get_lines_valid("one-file", "no-console", "uac-admin"):
            if isinstance(variable, Compile.InvalidVariable):
                return f"Error, line {variable.line}, Convert option \"{variable.value}\" invalid"
            if variable.value == "one-file":
                self.one_file = True
            elif variable.value == "no-console":
                self.console = False
            elif variable.value == "uac-admin":
                self.uac_admin = True

    def block_data(self, block_code):
        data = []
        for d in block_code.get_sources():
            if isinstance(d, Compile.InvalidVariable):
                return f"Error, line {d.line} value \"{d}\" invalid"
            if not d.dest_dir:
                return f"Error, line {d.line} DestDir not found"
            if not d.valid:
                return f"Error, line {d.line} No such file or directory \"{d.path.value}\""
            data.append((self.__remake_path(d.path.value), self.__remake_path(d.dest_dir)))
        self.data = data

    def block_pathex(self, block_code):
        pathex = []
        for d in block_code.get_sources():
            if isinstance(d, Compile.InvalidVariable):
                return f"Error, line {d.line} value \"{d}\" invalid"
            if d.dest_dir:
                return f"Error, line {d.line} DestDir not used"
            if not d.valid:
                return f"Error, line {d.line} No such file or directory \"{d.path.value}\""
            pathex.append(self.__remake_path(d.path.value))
        self.pathex = pathex

    def read_code(self):
        if "[Setup]" not in self.code:
            return "Error, [Setup] not found"
        action_blocks = {
            "Setup": self.block_setup,
            "Option": self.block_option,
            "Data": self.block_data,
            "Pathex": self.block_pathex
        }
        for code_block in self.__get_code_blocks("Setup", "Option", "Pathex", "Data"):
            mess =  action_blocks[code_block.name](code_block)
            if mess:
                return mess

    def run(self):
        self.pid = None
        error = self.read_code()
        if error:
            yield error
        else:
            if self.one_file:
                spec_file = SpecFile.one_file(self.input_file, self.pathex, self.binaries, self.data, self.hidden_imports, self.name, self.console, self.uac_admin, self.icon)
            else:
                spec_file = SpecFile.one_dir(self.input_file, self.pathex, self.binaries, self.data, self.hidden_imports, self.name, self.console, self.uac_admin, self.icon)
            p = subprocess.Popen(
                f'{self.converter} --clean --distpath="{self.output_dir}" --workpath="{path.source.join("build")}" "{spec_file}"',
                creationflags=subprocess.CREATE_NO_WINDOW,
                **self.__subprocess_args()
            )
            self.pid = p.pid
            for e in p.stderr:
                yield e.decode()[:-2]
