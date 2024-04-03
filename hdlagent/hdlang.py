
from abc import ABC, abstractmethod

class HDLang(ABC):
    @abstractmethod
    def extract_code(self, prompt: str) -> str:
        pass

    def extract_codeblock(self, text:str):
        if text is None:    # XXX - Deal with this better
            return ""
        if (text.count('```') == 0) or (text.count('```') % 2 != 0):
            return text
        lines   = text.split('\n')
        capture = False
        block   = []
        for line in lines:
            if line.strip().startswith('```'):
                if capture:
                    res_string = '\n'.join(block)
                    if res_string is None:
                        return ""
                    return res_string
                capture = True
                continue
            if capture:
                block.append(line)
        #if text.count('```') == 0:
        #    return text
        #capture = False
        #block   = ""
        #for line in text.splitlines():
        #    s = line.strip()
        #    if s.startswith('```'):
        #        capture = not capture
        #    if capture:
        #        block += s + "\n"
#
        #return block

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
        #print(f"raw {prompt}")
        txt = self.extract_codeblock(prompt).replace('\\', '')

        #print(f"from extract_codeblock {txt}")
        answer = ""
        capture = False
        for l in txt.splitlines():
            if ('struct' in l) or ('fn ' in l):
                capture = True
            if capture:
                if '```' in l:
                    return answer
                answer += l + "\n"

        if answer == "":
            answer = txt
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

