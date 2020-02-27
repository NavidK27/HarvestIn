from  exceptions import *
from  suffix_printer import *
from  extractors import *
from  generic import *

def harvest_contacts(args,session,main_profiles=[]):


    for company_name in args.company_names:


        try:
            cid = company_id = session.getCompanyId(company_name)
            esprint(f'Company Identifier for {company_name}: {cid}')
        except SessionException:
            esprint(f'Failed to get company identifier for {company_name} ' \
                    'Continuing to next company')

        esprint('Getting initial profiles')
        resp = session.getContactSearchResults(cid,0,10)

        count,profiles = extractInfo(resp.json(),company_name,cid)
        esprint(f'Available profiles: {count}')


        esprint('Extracting remaining profiles (this will take some time)')
        offset,max_facet_values = 10,10
        profiles = extractProfiles(session=session,
                company_name=company_name,
                company_id=cid,
                offset=offset,
                max_facet_values=max_facet_values)


        for profile in profiles:
            if profile not in main_profiles:
                main_profiles.append(profile)

    esprint(f'Done! Total known profiles: {main_profiles.__len__()}')

    esprint(f'Writing output to {args.output_file}')
    writeProfiles(args.output_file,main_profiles)
    esprint('Done!')
