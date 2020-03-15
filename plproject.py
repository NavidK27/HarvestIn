#!/usr/bin/env python3
import json
import argparse
import warnings
import csv
from sys import stdout, exit
from pathlib import Path
from parsers import *
from generators import *
from extractors import *
from session import Session
from args import parser as arg_parser
from suffix_printer import *
from generic import *
from exceptions import *
from constants import *
from harvest import harvest_contacts

warnings.filterwarnings('ignore')

args = arg_parser.parse_args()
if not args.cmd:
    arg_parser.print_help()
    exit()
headers = {'User-Agent':args.user_agent}

args.proxies = handleProxies(args.proxies)

if 'output_file' in args.__dict__:

    if args.output_file != stdout and Path(args.output_file).exists():
        esprint(f'Loading CSV file: {args.output_file}')
        main_profiles = loadProfiles(args.output_file)
        esprint(f'Total profiles loaded: {main_profiles.__len__()}')
    else:
        if args.output_file != stdout:
            esprint(f'Starting new CSV file: {args.output_file}')
        main_profiles = []
try:
    session = Session(headers=headers,
            proxies=args.proxies,
            verify=args.verify_ssl)

    esprint('Authenticating session')
    session.login(args)
    profile = session.getBasicProfile()

    if not session.authenticated:
        esprint('Authentication failed! Check credential settings ' \
                'and try again.')
        exit()

    if args.cmd == 'harvest_contacts':
        harvest_contacts(args,session,main_profiles)

    elif args.cmd == 'add_contacts':

        esprint('Sending connection requests, which will take '\
                'some time...')
        main_profiles = addContacts(session,main_profiles,args.message)
        esprint(f'Writing profiles to file: {args.output_file}')
        writeProfiles(args.output_file,main_profiles)

finally:
    if not args.cookies and not args.disable_logout:

        esprint('Logging out')
        session.getLogout()
        esprint('Done...exiting')
