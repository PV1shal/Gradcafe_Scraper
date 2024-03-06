class ProgramParser(object):
    def __init__(self, raw_string):
        self.raw_string = raw_string
        self.program, self.university = self.parse_h6_element()

    def parse_h6_element(self):
        h6_element = self.raw_string.find('h6', {'class': 'mt-3 fw-normal'})
        if h6_element:
            text_parts = [str(item) for item in h6_element.contents if isinstance(item, str)]
            result_text = ' '.join(text_parts).strip()
            program, university = result_text.split(',', 1)
            return program.strip(), university.strip()
        else:
            print("Error: 'h6' element not found.")
            return "", ""
    
    def get_program(self):
        return self.program

    def get_university(self):
        return self.university