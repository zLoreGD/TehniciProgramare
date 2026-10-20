from checker import build_url, is_https, show_response, check_site, scan_sites, check_headers, retry_check

#partea 1
print(build_url("/example.com","/login"))
print(is_https("https://example.com"))
print(is_https("http://example.com"))
#partea 2
show_response("https://httpbin.org/html")
#partea 3
print(check_site("https://httpbin.org/html"))

#partea 4
scan_sites()

#partea 5
print(check_headers("https://httpbin.org/html"))
#partea 6
print(retry_check("https://httpbin.org/status/200"))
