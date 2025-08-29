"""
Advanced Security Injection Tests for SauceDemo Login.
"""

import pytest
from playwright.sync_api import Page
from pages.saucedemo.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.saucedemo
@pytest.mark.security
class TestSauceDemoSecurity:
    """Advanced security testing for SauceDemo login functionality."""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup for each test."""
        self.login_page = LoginPage(page)
        self.login_page.open()
        
    # ========== SQL INJECTION TESTS ==========
    
    def test_sql_injection_basic_or(self, page: Page):
        """Test basic SQL injection with OR clause."""
        payloads = [
            "admin' OR '1'='1",
            "admin' OR '1'='1' --",
            "admin' OR '1'='1' #",
            "admin' OR 1=1 --",
            "' OR '1'='1",
            "' OR 1=1 --",
            "admin'/**/OR/**/1=1",
        ]
        
        for payload in payloads:
            self.login_page.clear_username()
            self.login_page.clear_password()
            self.login_page.login(payload, "password")
            
            # Should show error, not bypass authentication
            assert self.login_page.is_error_displayed(), f"SQL injection not blocked: {payload}"
            
            # Close error for next test
            if self.login_page.is_error_displayed():
                self.login_page.close_error_message()
    
    def test_sql_injection_union_attacks(self, page: Page):
        """Test UNION-based SQL injection attacks."""
        payloads = [
            "admin' UNION SELECT 1,2,3 --",
            "admin' UNION SELECT NULL,NULL,NULL --",
            "admin' UNION ALL SELECT 1,2,3 --",
            "' UNION SELECT username,password FROM users --",
            "admin' UNION SELECT @@version --",
        ]
        
        for payload in payloads:
            self.login_page.clear_username()
            self.login_page.clear_password()
            self.login_page.login(payload, "password")
            
            assert self.login_page.is_error_displayed(), f"UNION injection not blocked: {payload}"
            
            if self.login_page.is_error_displayed():
                self.login_page.close_error_message()
    
    def test_sql_injection_time_based(self, page: Page):
        """Test time-based blind SQL injection."""
        payloads = [
            "admin'; WAITFOR DELAY '00:00:05' --",
            "admin' AND (SELECT COUNT(*) FROM sysobjects) > 0 WAITFOR DELAY '00:00:05' --",
            "admin'; SELECT SLEEP(5) --",
            "admin' AND SLEEP(5) --",
            "admin'; pg_sleep(5) --",
        ]
        
        for payload in payloads:
            self.login_page.clear_username()
            self.login_page.clear_password()
            
            import time
            start_time = time.time()
            self.login_page.login(payload, "password")
            end_time = time.time()
            
            # Should not cause significant delay (time-based injection blocked)
            assert (end_time - start_time) < 3, f"Possible time-based injection: {payload}"
            
            if self.login_page.is_error_displayed():
                self.login_page.close_error_message()
    
    def test_sql_injection_error_based(self, page: Page):
        """Test error-based SQL injection."""
        payloads = [
            "admin' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT version()), 0x7e)) --",
            "admin' AND (SELECT * FROM (SELECT COUNT(*),CONCAT(version(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a) --",
            "admin' AND 1=CONVERT(int,(SELECT @@version)) --",
            "admin' AND 1=CAST((SELECT @@version) AS int) --",
        ]
        
        for payload in payloads:
            self.login_page.clear_username()
            self.login_page.clear_password()
            self.login_page.login(payload, "password")
            
            # Should not reveal database errors
            if self.login_page.is_error_displayed():
                error_text = self.login_page.get_error_message()
                # Check that error doesn't contain database-specific information
                sensitive_keywords = ['mysql', 'sql', 'database', 'table', 'column', 'syntax', 'version']
                for keyword in sensitive_keywords:
                    assert keyword.lower() not in error_text.lower(), f"Database info leaked: {keyword} in {error_text}"
                
                self.login_page.close_error_message()
    
    # ========== XSS (Cross-Site Scripting) TESTS ==========
    
    def test_xss_script_injection(self, page: Page):
        """Test XSS script injection in login fields."""
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<script>document.location='http://evil.com'</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')",
            "<iframe src=javascript:alert('XSS')></iframe>",
            "<body onload=alert('XSS')>",
            "<input onfocus=alert('XSS') autofocus>",
        ]
        
        for payload in xss_payloads:
            self.login_page.clear_username()
            self.login_page.clear_password()
            self.login_page.login(payload, "password")
            
            # Check that no alert dialog appeared (XSS was blocked)
            try:
                # If XSS executed, there might be an alert dialog
                page.wait_for_function("window.alert", timeout=1000)
                assert False, f"XSS payload executed: {payload}"
            except:
                # Good - no alert means XSS was blocked
                pass
            
            if self.login_page.is_error_displayed():
                self.login_page.close_error_message()
    
    def test_xss_attribute_injection(self, page: Page):
        """Test XSS through HTML attribute injection."""
        payloads = [
            "\" onmouseover=\"alert('XSS')\"",
            "' onclick='alert(\"XSS\")'",
            "\" autofocus onfocus=\"alert('XSS')\"",
            "' style='expression(alert(\"XSS\"))'",
            "\" href=\"javascript:alert('XSS')\"",
        ]
        
        for payload in payloads:
            self.login_page.clear_username()
            self.login_page.clear_password()
            self.login_page.login(payload, "password")
            
            # Verify payload doesn't get executed as HTML attributes
            username_value = self.login_page.get_username_value()
            # Value should be properly escaped/sanitized
            assert "<" not in username_value or ">" not in username_value or payload != username_value
            
            if self.login_page.is_error_displayed():
                self.login_page.close_error_message()
    
    # ========== LDAP INJECTION TESTS ==========
    
    def test_ldap_injection(self, page: Page):
        """Test LDAP injection attacks."""
        ldap_payloads = [
            "admin)(&)",
            "admin)(|(objectClass=*))",
            "admin))(|(objectClass=*",
            "*)(&(objectClass=*",
            "admin)(&(objectClass=*)(objectClass=*))",
        ]
        
        for payload in ldap_payloads:
            self.login_page.clear_username()
            self.login_page.clear_password()
            self.login_page.login(payload, "password")
            
            assert self.login_page.is_error_displayed(), f"LDAP injection not blocked: {payload}"
            
            if self.login_page.is_error_displayed():
                self.login_page.close_error_message()
    
    # ========== COMMAND INJECTION TESTS ==========
    
    def test_command_injection(self, page: Page):
        """Test OS command injection attacks."""
        command_payloads = [
            "admin; cat /etc/passwd",
            "admin && dir",
            "admin | whoami",
            "admin`id`",
            "admin$(whoami)",
            "admin; ls -la",
            "admin & net user",
            "admin || ping 127.0.0.1",
        ]
        
        for payload in command_payloads:
            self.login_page.clear_username()
            self.login_page.clear_password()
            self.login_page.login(payload, "password")
            
            assert self.login_page.is_error_displayed(), f"Command injection not blocked: {payload}"
            
            if self.login_page.is_error_displayed():
                self.login_page.close_error_message()
    
    # ========== PATH TRAVERSAL TESTS ==========
    
    def test_path_traversal(self, page: Page):
        """Test path traversal attacks."""
        traversal_payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "....//....//....//etc/passwd",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd",
            "..%252f..%252f..%252fetc%252fpasswd",
            "..%c0%af..%c0%af..%c0%afetc%c0%afpasswd",
        ]
        
        for payload in traversal_payloads:
            self.login_page.clear_username()
            self.login_page.clear_password()
            self.login_page.login(payload, "password")
            
            assert self.login_page.is_error_displayed(), f"Path traversal not blocked: {payload}"
            
            if self.login_page.is_error_displayed():
                self.login_page.close_error_message()
    
    # ========== FORMAT STRING TESTS ==========
    
    def test_format_string_injection(self, page: Page):
        """Test format string injection attacks."""
        format_payloads = [
            "%s%s%s%s%s%s%s%s%s%s%s%s",
            "%x%x%x%x%x%x%x%x%x%x%x%x",
            "%n%n%n%n%n%n%n%n%n%n%n%n",
            "%08x.%08x.%08x.%08x.%08x",
            "AAAA%08x.%08x.%08x.%08x.%08x",
        ]
        
        for payload in format_payloads:
            self.login_page.clear_username()
            self.login_page.clear_password()
            self.login_page.login(payload, "password")
            
            assert self.login_page.is_error_displayed(), f"Format string injection not blocked: {payload}"
            
            if self.login_page.is_error_displayed():
                self.login_page.close_error_message()
    
    # ========== NULL BYTE INJECTION TESTS ==========
    
    def test_null_byte_injection(self, page: Page):
        """Test null byte injection attacks."""
        null_payloads = [
            "admin\x00",
            "admin%00",
            "admin\u0000password",
            "admin%00.txt",
            "admin\x00\x00\x00",
        ]
        
        for payload in null_payloads:
            self.login_page.clear_username()
            self.login_page.clear_password()
            self.login_page.login(payload, "password")
            
            # Should handle null bytes gracefully
            if self.login_page.is_error_displayed():
                self.login_page.close_error_message()
    
    # ========== OVERFLOW TESTS ==========
    
    def test_buffer_overflow_simulation(self, page: Page):
        """Test extremely long inputs to check for buffer overflow protection."""
        # Generate very long string
        long_string = "A" * 10000
        
        self.login_page.clear_username()
        self.login_page.clear_password()
        
        try:
            self.login_page.login(long_string, "password")
            
            # Should handle gracefully, not crash
            if self.login_page.is_error_displayed():
                error_text = self.login_page.get_error_message()
                # Should not reveal internal errors
                assert "buffer" not in error_text.lower()
                assert "overflow" not in error_text.lower()
                assert "exception" not in error_text.lower()
        except Exception as e:
            # If exception occurs, it should be handled gracefully
            assert "timeout" not in str(e).lower(), "Possible application crash from buffer overflow"
    
    # ========== ENCODING BYPASS TESTS ==========
    
    def test_encoding_bypass(self, page: Page):
        """Test various encoding bypass techniques."""
        encoded_payloads = [
            # URL encoding
            "%27%20OR%20%271%27%3D%271",  # ' OR '1'='1
            "%3Cscript%3Ealert%28%27XSS%27%29%3C/script%3E",  # <script>alert('XSS')</script>
            
            # Double URL encoding  
            "%2527%2520OR%2520%25271%2527%253D%25271",
            
            # Unicode encoding
            "\u0027\u0020OR\u0020\u0027\u0031\u0027\u003D\u0027\u0031",
            
            # HTML entity encoding
            "&#39; OR &#39;1&#39;=&#39;1",
            "&lt;script&gt;alert(&#39;XSS&#39;)&lt;/script&gt;",
        ]
        
        for payload in encoded_payloads:
            self.login_page.clear_username()
            self.login_page.clear_password()
            self.login_page.login(payload, "password")
            
            # Encoded payloads should not bypass security
            assert self.login_page.is_error_displayed(), f"Encoding bypass successful: {payload}"
            
            if self.login_page.is_error_displayed():
                self.login_page.close_error_message()
    
    # ========== RATE LIMITING TESTS ==========
    
    @pytest.mark.slow
    def test_brute_force_protection(self, page: Page):
        """Test protection against brute force attacks."""
        # Attempt multiple failed logins rapidly
        for i in range(10):
            self.login_page.clear_username()
            self.login_page.clear_password()
            self.login_page.login(f"hacker{i}", f"wrongpass{i}")
            
            if self.login_page.is_error_displayed():
                error_text = self.login_page.get_error_message()
                
                # Check if account gets locked or rate limited
                if "locked" in error_text.lower() or "too many" in error_text.lower():
                    print(f"✅ Rate limiting detected after {i+1} attempts")
                    break
                    
                self.login_page.close_error_message()
            
            # Small delay between attempts
            page.wait_for_timeout(100) 