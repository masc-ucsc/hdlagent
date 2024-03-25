
from abc import ABC, abstractmethod

class HDLang(ABC):
    @abstractmethod
    def extract_code(self, prompt: str) -> str:
        pass

    def extract_codeblock(self, text:str):
        if text.count('```') == 0:
            return text
        capture = False
        block   = ""
        for line in text.splitlines():
            s = line.strip()
            if s.startswith('```'):
                capture = not capture
            if capture:
                block += s + "\n"

        return block

class HDLang_verilog(HDLang):
    def extract_code(self, prompt: str) -> str:
        txt = self.extract_codeblock(prompt)

        answer = ""
        in_module = False
        for l in txt.splitlines():
            if in_module:
                answer += l + "\n"
                if "endmodule" in l:
                    in_module = False
            else:
                s = l.strip()
                if s.startswith('`include') or s.startswith('`define') or s.startswith('`if') or s.startswith('`else') or s.startswith('`endif'):
                    answer += s
                elif "module" in l:
                    in_module = True
                    answer += s + "\n"

        return answer

class HDLang_chisel(HDLang):
    def extract_code(self, prompt: str) -> str:
        txt = self.extract_codeblock(prompt)
        return txt

class HDLang_pyrtl(HDLang):
    def extract_code(self, prompt: str) -> str:
        txt = self.extract_codeblock(prompt)
        return txt

class HDLang_dslx(HDLang):
    def extract_code(self, prompt: str) -> str:
        txt = self.extract_codeblock(prompt)

        answer = ""
        capture = False
        for l in txt.splitlines():
            if 'struct' in l:
                capture = True
            if capture:
                answer += l + "\n"

        return answer

def get_hdlang(lang: str) -> HDLang:
    l = lang.lower()
    if l == "verilog":
        return HDLang_verilog()
    elif l == "chisel":
        return HDLang_chisel()
    elif l == "pyrtl":
        return HDLang_pyrtl()
    elif l == "dslx":
        return HDLang_dslx()
    else:
        raise ValueError("Unsupported Language type in HDLang")

#hdlang = get_hdlang("VerIloG")

