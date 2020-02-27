from  profile import Profile
from  exceptions import SessionException
from  suffix_printer import *
from  constants import *
from re import sub

def extractInfo(j,company_name,company_id):

    result_count = j['metadata']['totalResultCount']
    to_parse = []
    for e in j['elements']:

        if 'hitInfo' in e and 'com.linkedin.voyager.search.SearchProfile' in \
                e['hitInfo']:
                    to_parse.append(e)

    return (result_count,
            [extractProfile(e,company_name,company_id)
                for e in to_parse])

def extractProfile(jelement,company_name,company_id):

    j = jelement

    try:

        profile = j['hitInfo'] \
                ['com.linkedin.voyager.search.SearchProfile']

        industry = profile.get('industry')
        location = profile.get('location')

        mini_profile = profile['miniProfile']
        first_name = mini_profile['firstName']
        last_name = mini_profile['lastName']
        occupation = mini_profile['occupation']
        public_identifier = mini_profile['publicIdentifier']
        entity_urn = mini_profile['entityUrn']

    except Exception as e:

        esprint('Failed to parse profile from JSON!',suf='[!]')
        raise e

    if entity_urn:
        try:
            entity_urn = entity_urn.split(':')[-1]
        except:
            entity_urn = None

    return Profile(first_name, last_name, occupation, public_identifier,
            industry, location, entity_urn, company_name, company_id)

def extractProfiles(session,company_name,company_id,offset=10,
        max_facet_values=10):


    profiles = []
    while True:


        try:

            resp = session.getContactSearchResults(company_id,
                    offset,max_facet_values)

            if resp.status_code != 200 or 'Content-Type' not in \
                    resp.headers or resp.headers['Content-Type'] != \
                    CONTENT_TYPE_APPLICATION_JSON:
                raise SessionException('Invalid API response received')

        except Exception as e:

            esprint('Failed to get search results',suf='[!]')
            print('Exception Message:',e)
            return profiles

        try:

            icount,iprofiles = extractInfo(resp.json(),
                company_name,company_id)

        except Exception as e:

            esprint('Failed to extract search results',suf='[!]')
            print('Exception Message:',e)
            raise profiles

        profiles += iprofiles
        if offset >= icount or offset >= 999: break
        offset += max_facet_values
        if offset >= 1000: offset = 999

    return profiles
