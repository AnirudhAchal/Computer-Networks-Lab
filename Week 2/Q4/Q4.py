# Import required libraries
import requests
from re import compile

# Formatting related variables
BOLD_START = '\033[1m'
ITALIC_START = '\033[3m'
STYLE_END = '\033[0m'

# Input a valid URL from the user
url = ""
pattern = compile("^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$")
while not pattern.match(url):
    url = input("Enter the URL to find data for: ")

if url[:7] != "http://" and url[:8] != "https://":
    url = "http://" + url

# Try to get the HTML data from the input URL
try:
    req = requests.get(url)
except:
    print("Invalid URL!")
    exit(1)

# Print the response status code
print(f"{BOLD_START}\nStatus Code:{STYLE_END} {req.status_code}")

# Print the response reason
print(f"{BOLD_START}Reason:{STYLE_END} {req.reason}")

# Print the response encoding
print(f"{BOLD_START}Encoding:{STYLE_END} {req.encoding}")

# Print the Round Trip Time in milliseconds
print(f"{BOLD_START}Elapsed Time:{STYLE_END} {req.elapsed.microseconds / 10**3}ms")

# Print the response headers
print(f"\n{BOLD_START}Headers:{STYLE_END}")
for header in req.headers:
    print(f"{header}: {req.headers[header]}")

# Print the response history
print(f"\n{BOLD_START}History:{STYLE_END}")
for ele in req.history:
    print(ele.status_code, ele.reason)

# Print the cookies associated with the response
print(f"\n{BOLD_START}Cookies:{STYLE_END}")
for cookie in req.cookies:
    print(cookie)

# Print the request headers
print(f"\n{BOLD_START}Request:{STYLE_END} {req.request.method} Request to {req.request.url}")
print(f"{BOLD_START}Request Headers:{STYLE_END}")
for header in req.request.headers:
    print(f"{header}: {req.request.headers[header]}")
