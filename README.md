# HarvestIn

## Contributors:

- [Navid Kagalwalla](https://github.com/NavidK27)
- [Akash Dubey](https://github.com/Sparkton)

HarvestIn is a LinkedIn Recon Tool which authenticates to the LinkedIn API and uses the API to perform several tasks such as:
 - Harvest Information from Profiles
 - Automated Connection Requests
 
# Usage

## Profile Harvesting

By supplying one or more company names to the `harvest` command,
HarvestIn will make API calls to acquire the numeric identifier of
a target company identifier and proceed to enumerate employees
from the people section of the target company.

### Example

If the target is Starbucks and the company name was
found to be `starbucks` via search engine, then the
following command would attempt to harvest profiles and write CSV
records to starbucks.csv:

_WARNING_: Use of the `-ac` flag will result in a connection request
being sent to each accessible profile.If you wish to filter for
particlar profiles, use the `-of` flag to dump the results to disk
and select specific records via grep and use the `add_contacts`
subcommand to create connection requests.

```
Navids-MacBook-Pro:HarvestIn navidkagalwalla$ export creds='username':'password'
Navids-MacBook-Pro:HarvestIn navidkagalwalla$ ./plproject.py harvest -C "$creds" -cns starbucks -of starbucks.csv

[+] Starting new CSV file: starbucks.csv
[+] Authenticating session
[+] Company Identifier for starbucks: 2271
[+] Getting initial profiles
[+] Available profiles: 131173
[+] Extracting remaining profiles (this will take a bit)
[+] Done! Total known profiles: 332
[+] Writing output to starbucks.csv
[+] Done!
[+] Logging out
[+] Done...exiting

```
### Limitations

LinkedIn will allow only the first 1,000 search results to be
returned when harvesting contact information, however the same
results are not returned each time a series of searches are
applied. Run the harvest command multiple times to capture more
contacts.
To increase the number of contacts a given profile
can access:
- Generate connection requests for company people via the `add_contacts`
subcommand or the `-ac` flag of the `harvest` command

## Connection Request Generation

Use the `add_contacts` subcommand to generate connection requests for
target profiles. This command takes the name of a CSV file generated
by the `harvest` subommand and will indiscriminately send a connection
request for each record.

### Example

To send a connection request to each of the profiles enumerated from 
Starbucks, run the following command. After execution, visit
the `My Network` tab of your LinkedIn profile to observe the connection
requests.

```

Navids-MacBook-Pro:HarvestIn navidkagalwalla$ ./plproject.py add_contacts -if starbucks.csv -C "$creds"

[+] Loading CSV file: starbucks.csv
[+] Total profiles loaded: 332
[+] Authenticating session
[+] Sending connection requests, which will take some time...
[+] Sending Connection Request 1: Shawn Harris, Principal Enterprise Security Architect @ starbucks
[+] Sending Connection Request 2:  , Director HR at TE Connectivity @ starbucks
[+] Writing profiles to file: starbucks.csv
[+] Logging out
[+] Done...exiting
```


