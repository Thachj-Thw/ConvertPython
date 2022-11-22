import compiler
from app import App


class Run(App):
    def __init__(self):
        super().__init__()
        self._thread = None

    def _start_convert(self):
        self._save_file()
        self._thread = compiler.CompileInThread(self, self.txe_code.toPlainText(), self._file)
        self._thread.output.connect(self._logs)
        self._thread.end.connect(self._on_end)
        self._thread.start()

    def _is_converting(self):
        if self._thread and self._thread.isRunning():
            return True
        return False

    def _stop_convert(self):
        if self._thread:
            pid = self._thread.stop()
            self.txe_out.insertHtml(f'<span style="font-size: 13px; font-weight: 400; color: #cf2727; font-style: normal; white-space: pre-wrap;">STOP\n</span>')
            self._alert("Convert stopped!" + f" end process id {pid}" if pid is not None else "")

    def _on_end(self, end_out):
        if "Building EXE from EXE-00.toc completed successfully" in end_out:
            self._alert(end_out)
        else:
            self._error_message("Convert failed!\n" + end_out)
