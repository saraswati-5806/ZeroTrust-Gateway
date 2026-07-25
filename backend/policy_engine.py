"""
Zero Trust Policy Evaluation Engine

Evaluates 5 independent security signals.

Signals:
1. RBAC
2. Device Posture
3. Time Policy
4. Geo Location
5. AI Risk Score

Returns

{
    "allow": True/False,
    "score": int,
    "reasons":[]
}
"""

from datetime import datetime


class PolicyEngine:

    def __init__(self):

        self.allowed_roles = {
            "Admin",
            "Developer",
            "Manager",
            "Employee"
        }

        self.allowed_countries = {
            "India",
            "Singapore"
        }

        self.office_start = 8
        self.office_end = 20

    # -------------------------------------------------

    def check_role(self, user):

        role = user.get("role")

        if role in self.allowed_roles:
            return True, "Role Verified"

        return False, "Invalid Role"

    # -------------------------------------------------

    def check_device(self, device):

        healthy = device.get("healthy", False)
        encrypted = device.get("encrypted", False)
        antivirus = device.get("antivirus", False)

        if healthy and encrypted and antivirus:
            return True, "Trusted Device"

        return False, "Device Security Failed"

    # -------------------------------------------------

    def check_time(self):

        current_hour = datetime.now().hour

        if self.office_start <= current_hour <= self.office_end:
            return True, "Office Hours"

        return False, "Outside Allowed Hours"

    # -------------------------------------------------

    def check_location(self, location):

        country = location.get("country")

        if country in self.allowed_countries:
            return True, "Approved Country"

        return False, "Restricted Country"

    # -------------------------------------------------

    def check_ai_score(self, score):

        """
        Lower score means lower risk.

        0-40   Safe
        41-70  Medium
        71+    High Risk
        """

        if score <= 40:
            return True, "Low AI Risk"

        return False, "High AI Risk"

    # -------------------------------------------------

    def evaluate(self, request_data):

        score = 0
        reasons = []

        checks = [

            self.check_role(
                request_data["user"]
            ),

            self.check_device(
                request_data["device"]
            ),

            self.check_time(),

            self.check_location(
                request_data["location"]
            ),

            self.check_ai_score(
                request_data["ai_score"]
            )

        ]

        for passed, message in checks:

            reasons.append(message)

            if passed:
                score += 20

        return {

            "allow": score == 100,
            "score": score,
            "reasons": reasons

        }


policy_engine = PolicyEngine()