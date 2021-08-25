import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="google-apis-oauth-django",
    version="1.0.0",
    author="Nishant Mittal",
    author_email="admin@nishantwrp.com",
    description="A library to help integrate Google OAuth 2.0 to your Django application.",
    license = 'MIT License',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nishantwrp/google-apis-oauth-django",
    install_requires=[
        'google-auth-httplib2', 'google-auth-oauthlib'
    ],
    packages=setuptools.find_packages()
)
