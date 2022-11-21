import dns.resolver
import sys
import re
import os

# List of dns record types to try
record_types=['A','AAAA','ALIAS','CNAME','MX','NS','PTR','SOA','SRV','TXT']
# List to hold the records that will be later written to a .csv.
records=[]

# Get the target domain, if the argument is not provided then warn and exit.
try:
    target=sys.argv[1]
except:
    print("[!] Provide the domain you want to target as an argument. (e.g: python3 ./Tools/dns-enum.py ccnb.ca)")
    exit()

# Get the subdomains list file as the second argument, if the argument is not provided or the path to the list is wrong then no subdomain is set and the code
# still runs.
try:
    subdomain_list=sys.argv[2]
    f=open(subdomain_list,'r')
    subdomains=f.readlines()
    f.close()
except:
    print("[!] A subdomains list was either not provided or not found. (Provide the path to the subdomains list as the second argument)")
    subdomains=[""]

# For each provided subdomain run a dns query of each type.
for subdomain in subdomains:
    subdomain=re.sub("\n","",subdomain)
    for type in record_types:
                try:
                    answer = dns.resolver.resolve(subdomain+"."+target, type)
                    for server in answer:
                            record=subdomain+","+type+","+server.to_text()
                            records.append(record)
                except:
                    pass

# Remove the old results if they exist.
try:
    os.remove('./Scans/%s/dnsEnum-%s.csv'%(target,target))
except:
    pass

#records=[*set(records)] # Remove duplicates (debug)
# Write results to a csv file.
with open('./Scans/%s/dnsEnum-%s.csv'%(target,target), 'a') as f:
    f.write("Subdomain,Type,Record\n")
    for record in records:
        f.write(record+"\n")
    f.close()