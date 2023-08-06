from .base import AppFactory, User


def github_fetch_user(client):
    resp = client.get('user')
    profile = resp.json()
    uid = profile.get('id')
    username = profile.get('login')
    name = profile.get('name')
    email = profile.get('email')
    return User(uid, username=username, name=name, email=email)


github = AppFactory('github', {
    'api_base_url': 'https://api.github.com/',
    'access_token_url': 'https://github.com/login/oauth/access_token',
    'authorize_url': 'https://github.com/login/oauth/authorize',
    'client_kwargs': {'scope': 'user:email'},
    'fetch_user': github_fetch_user,
}, "The OAuth app for GitHub API.")
