import re

AMERICAN = "American"
INTERNATIONAL = "International"
OTHER = "Other"
UNKNOWN = "Unknown"
WAITLISTED = "Waitlisted"
REJECTED = "Rejected"
ACCEPTED = "Accepted"

term_pattern = r'(Fall|Summer)\s\d{4}'
applicant_type_pattern = r'(?i)AMERICAN|INTERNATIONAL|OTHER|UNKNOWN'
gre_pattern = r'GRE\s(\d{1,3})'
gre_awa_pattern = r'GRE\sAW\s(\d{1,2}\.\d{1,2})'
gre_verbal_pattern = r'GRE\sV\s(\d{1,3})'
gpa_pattern = r'GPA\s(\d{1,2}\.\d{1,2})'
degree_pattern = r'(?i)Masters|PhD|Other'
status_pattern = r'(?i)Waitlisted|Rejected|Accepted'


class CredentialParser(object):
    def __init__(self, raw_row):
        self.raw_row = raw_row
        self.parsed_data = self.parse_cred_data()

    def parse_applicant_status(self):
        data = self.raw_row.find_all('span', {'class': re.compile(r'badge badge-(.+)')})
        if data:
            color = data[0]['class'][1]
            if color == 'badge-green':
                return "Accepted"
            elif color == 'badge-red':
                return "Rejected"
            elif color == 'badge-blue':
                return "Waitlisted"
        return ""

    def parse_cred_data(self):
            data = {
                "Term": "",
                "GRE": "",
                "GRE V": "",
                "GRE AW": "",
                "GPA": "",
                "Degree": "",
                "Applicant type": "",
                "Status": ""
            }
            for info in self.raw_row.find_all('span', {'class': 'badge badge-unselected'}):
                text = info.getText()
                # print(text)

                term_match = re.search(term_pattern, text)
                applicant_type_match = re.search(applicant_type_pattern, text)
                gre_match = re.search(gre_pattern, text)
                gre_verbal_match = re.search(gre_verbal_pattern, text)
                gre_awa_match = re.search(gre_awa_pattern, text)
                gpa_match = re.search(gpa_pattern, text)
                degree_match = re.search(degree_pattern, text)
                status_match = re.search(status_pattern, text)

                if term_match:
                    data["Term"] = term_match.group()

                if applicant_type_match:
                    data["Applicant type"] = applicant_type_match.group()

                if gre_match:
                    data["GRE"] = int(gre_match.group(1))

                if gre_verbal_match:
                    data["GRE V"] = int(gre_verbal_match.group(1))

                if gre_awa_match:
                    data["GRE AW"] = float(gre_awa_match.group(1))

                if gpa_match:
                    data["GPA"] = float(gpa_match.group(1))

                if degree_match:
                    data["Degree"] = degree_match.group()
                    
                if status_match:
                    data["Status"] = status_match.group()
            return data

    def parse_gpa(self):
        return self.parsed_data["GPA"]

    def parse_gre_verbal(self):
        return self.parsed_data["GRE V"]

    def parse_gre_quant(self):
        return self.parsed_data["GRE"]

    def parse_gre_awa(self):
        return self.parsed_data["GRE AW"]
    
    def parse_degree(self):
        return self.parsed_data["Degree"]
    
    def parse_applicant_type(self):
        return self.parsed_data["Applicant type"]
    
    def parse_status(self):
        return self.parsed_data["Status"]
    
    def parse_season(self):
        return self.parsed_data["Term"].split(" ")[0]
    
    def parse_term_year(self):
        return self.parsed_data["Term"].split(" ")[1]
