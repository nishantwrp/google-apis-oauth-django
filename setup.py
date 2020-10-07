import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="google-apis-oauth-django",
    version="0.0.1",
    author="Nishant Mittal",
    author_email="admin@nishantwrp.com",
    description="TODO",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nishantwrp/google-apis-oauth-django",
    install_requires=[
        'google-auth-httplib2', 'google-auth-oauthlib'
    ],
    packages=setuptools.find_packages()
)
