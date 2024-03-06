from parsers.credential_parser import CredentialParser
from parsers.program_parser import ProgramParser


class Parser:

    def __init__(self):
        self.parsed_data = []

    def parse(self, table):
        for row in table:
            program_parser = ProgramParser(row)
            credential_parser = CredentialParser(row)
            
            try:
                parsed_row = {
                    'university': program_parser.get_university(),
                    'major': program_parser.get_program(),
                    'season': credential_parser.parse_season(),
                    'term_year': credential_parser.parse_term_year(),
                    'undergrad_gpa': credential_parser.parse_gpa(),
                    'gre_verbal': credential_parser.parse_gre_verbal(),
                    'gre_quant': credential_parser.parse_gre_quant(),
                    'gre_awa': credential_parser.parse_gre_awa(),
                    'degree': credential_parser.parse_degree(),
                    'decision': credential_parser.parse_status(),
                    'applicant_status': credential_parser.parse_applicant_status(),
                }
                # parsed_row = {k: self.__parse(v) for k, v in parsed_row.items()}
                # print(parsed_row)
                self.parsed_data.append(parsed_row)
            except:
                continue
        # print(self.parsed_data)
        return self.parsed_data

    @staticmethod
    def __parse(data):
        if data is None:
            return ""
        else:
            return data.encode('ascii', 'ignore').decode('ascii')
