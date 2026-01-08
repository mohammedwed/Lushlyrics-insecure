Lushlyrics: Secure Authentication System Implementation
Project Overview
This project is a modified and secured version of the Lushlyrics (Youttify) web application. The primary goal was to transform an insecure application into a robust system by implementing industry-standard security practices using the Django framework.

Key Security Fixes & Features
1. Secure User Authentication
Password Hashing: Replaced insecure manual input handling with Django’s UserCreationForm. Passwords are now automatically hashed using the PBKDF2 algorithm with a SHA256 hash, ensuring that user data is protected even if the database is compromised.

Session Management: Utilized Django’s built-in auth system for secure login and logout workflows.

2. CSRF Protection
Added {% csrf_token %} to all registration, login, and password recovery forms. This prevents Cross-Site Request Forgery attacks, ensuring that all state-changing requests are intentional and come from authenticated users.

3. Access Control (Authorization)
Implemented the @login_required decorator for sensitive views such as Playlist and Search. Anonymous users are now automatically redirected to the login page, protecting user-specific content.

4. Reliability & Bug Fixes
Profile Management: Resolved the common DoesNotExist error by implementing get_or_create logic in the views. This ensures that every authenticated user has a corresponding profile in the database without system crashes.

5. Account Recovery
Integrated a secure Password Reset workflow, fulfilling the requirement for users to recover accounts via secure tokens.
