import re
import logging
from abc import ABC, abstractmethod


class HDLang(ABC):
    @abstractmethod
    def extract_code(self, prompt: str, verilog_path: str) -> str:
        pass

    # def extract_codeblock(self, text:str):
    #     if text is None:    # XXX - Deal with this better
    #         return ""
    #     if (text.count('```') == 0) or (text.count('```') % 2 != 0):
    #         return text.replace('```','')
    #     lines   = text.split('\n')
    #     capture = False
    #     block   = []
    #     for line in lines:
    #         if line.strip().startswith('```'):
    #             if capture:
    #                 res_string = '\n'.join(block)
    #                 if res_string is None:
    #                     return ""
    #                 return res_string
    #             capture = True
    #             continue
    #         if capture:
    #             block.append(line)

    def extract_codeblock(self, text: str) -> str:
        logging.debug("Starting extract_codeblock")
        if text is None:
            logging.debug("Text is None")
            return ""
        
        pattern = re.compile(r'```(?:\w+)?\n?([\s\S]*?)```', re.MULTILINE)
        matches = pattern.findall(text)
        logging.debug(f"Found {len(matches)} code block(s)")
        
        if matches:
            code = '\n\n'.join(match.strip() for match in matches)
            logging.debug("Extracted code using regex")
        else:
            code = text.replace('```', '').strip()
            logging.debug("No code blocks found, stripped backticks")
        
        code = code.replace('`', '')
        logging.debug("Removed any remaining backticks")
        
        return code

class HDLang_verilog(HDLang):
    # def extract_code(self, prompt: str, verilog_path: str) -> str:
    #     txt = self.extract_codeblock(prompt)
    #     txt = txt.replace('\\', '')

    #     answer = ""
    #     in_module = False
    #     for l in txt.splitlines():
    #         if in_module:
    #             answer += l + "\n"
    #         else:
    #             s = l.strip()
    #             if s.startswith('`include') or s.startswith('`define') or s.startswith('`if') or s.startswith('`else') or s.startswith('`endif'):
    #                 answer += s
    #             elif "module " in l:
    #                 in_module = True
    #                 answer += s + "\n"

    #         if "endmodule" in l: # Same line can have module and endmodule
    #             in_module = False

    #     return answer
    def extract_code(self, prompt: str, verilog_path: str) -> str:
        print("HDLang_verilog.extract_code called")
        txt = self.extract_codeblock(prompt)
        txt = txt.replace('\\', '')
        logging.debug(f"Extracted text: {txt}")
        
        answer = ""
        in_module = False
        for l in txt.splitlines():
            if in_module:
                answer += l + "\n"
            else:
                s = l.strip()
                if (s.startswith('`include') or s.startswith('`define') or
                    s.startswith('`if') or s.startswith('`else') or
                    s.startswith('`endif')):
                    answer += s + "\n"
                elif "module " in l:
                    in_module = True
                    answer += s + "\n"
            
            if "endmodule" in l:
                in_module = False
        
        logging.debug(f"Final extracted Verilog code: {answer}")
        return answer

class HDLang_chisel(HDLang):
    def extract_code(self, prompt: str, verilog_path: str) -> str:
        txt = self.extract_codeblock(prompt)
        txt = txt.replace('\\', '')

        answer  = ""
        capture = False
        for l in txt.splitlines():
            if 'import chisel' in l:
                capture = True
            if capture:
                answer += l + "\n"

        if answer == "":
            answer = txt
        return answer

class HDLang_pyrtl(HDLang):
    def extract_code(self, prompt: str, verilog_path: str) -> str:
        txt = self.extract_codeblock(prompt)
        txt = txt.replace('\\', '')

        answer  = ""
        capture = False
        for l in txt.splitlines():
            if 'import pyrtl' in l:
                capture = True
            if capture:
                answer += l + "\n"

        if answer == "":
            answer = txt

        pattern = r"(with open\()(.*?)(, 'w')"
        if re.search(pattern, answer):
            replacement = r"\1" + '\'' + str(verilog_path) + '\'' + r"\3"
            return re.sub(pattern, replacement, answer)
        return answer

class HDLang_dslx(HDLang):
    def extract_code(self, prompt: str, verilog_path: str) -> str:
        txt = self.extract_codeblock(prompt)
        txt = txt.replace('\\', '')

        answer  = ""
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


# hdlang = get_hdlang("VerIloG")

