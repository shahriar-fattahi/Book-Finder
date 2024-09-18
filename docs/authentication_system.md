# Authentication System

In this project, I use a token-based authentication system with the [Knox package](https://github.com/jazzband/django-rest-knox), which offers several advantages over the default system in Django Rest Framework (DRF):

- **Multiple Tokens**: DRF allows only one token per user, making it hard to securely sign in from multiple devices. Knox provides a unique token for each login, allowing every device to have its own token, which is securely deleted when the user logs out.

- **Token Management**: With Knox, users can log out from all devices at once by removing all tokens from the server, forcing all clients to re-authenticate.

- **Secure Token Storage**: DRF stores tokens in plain text, which could be a security risk if the database is compromised. Knox stores tokens in a secure hashed form, making it much harder for attackers to misuse them, even if the database is breached.

- **Token Expiration**: DRF tokens do not expire by default. Knox tokens can be configured to automatically expire after a set time (default is 10 hours), enhancing security.

## Why I Chose Token-Based Authentication

When deciding on the authentication system for this project, I considered three main options:

1. **JWT (JSON Web Token) Authentication**
2. **Session-Based Authentication**
3. **Token-Based Authentication**

### Why Not JWT?

While JWT authentication is faster because it doesn’t rely on the database for every request, it's mostly used for external services (when third-party services need to access our API). Since this project serves as the backend for a frontend application, JWT isn’t the best choice here.

A key security issue with JWT is that if a user's token is exposed, there’s no way to revoke it immediately. You either have to wait for the token to expire or change the secret key, which would invalidate all users’ tokens, causing unwanted disruption.

### Why Not Session-Based Authentication?

Session-based authentication can be a good choice when all requests come from the same context (like the frontend). It offers security against CSRF attacks, provided you implement proper protections.

However, the main advantage of session-based authentication is its ability to manage anonymous users easily. Since our project only allows authenticated users to interact with the API, this benefit doesn't apply here. I initially implemented session-based authentication but realized it wasn’t the most suitable for this project.

### Why Token-Based Authentication?

Token-based authentication offers a secure and efficient way for the frontend and backend to communicate. When the user logs in, they receive a token, which can be stored locally (e.g., in the browser’s local storage). This token is then manually sent with each request, reducing the risk of CSRF attacks since it’s not automatically included with every request.

If a user’s token is compromised, it can be easily revoked from the server-side by deleting it from the database, instantly invalidating the token.

For this small project, token-based authentication is both fast and secure, making it an ideal choice.
