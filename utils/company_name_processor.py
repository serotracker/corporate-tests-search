def get_processed_companies(company_list):
    processed_companies = []
    string_to_remove = ['Inc.', 'Incorporated', 'Corp.', 'Corporation', 'Ltd.', 'Limited']
    for company in company_list:
        company = company.split()
        processed_company = []
        for word in company:
            if len(company) == 2:
                processed_company.append(word)
            else:
                if word not in string_to_remove:
                    processed_company.append(word)
        processed_company = ' '.join(processed_company)
        processed_companies.append(processed_company)
    return processed_companies
