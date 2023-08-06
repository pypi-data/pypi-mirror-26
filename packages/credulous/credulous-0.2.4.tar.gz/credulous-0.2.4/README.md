# PyCredulous 

Manage your Google API credentials (Copy of PHP [Credulous](https://github.com/Brainlabs-Digital/credulous) by ryutaro@brainlabsdigital.com)

## Installation

```bash
pip install credulous
```

## Getting access and refresh tokens

On Linux/Mac, make sure you have credulous installed in you environment and run:

```bash
credulous --secret path/to/your/client_secret.json path/to/scopes
```

You will be asked to go to a URL on your browser, where you will do the
authorization and receive a code. Copy this into the prompt. You should now
have your access token and refresh token in your credentials file.

## Running with Options

The following command line options are now supported:

```bash
credulous -c --secret path/to/your/client_secret.json path/to/scopes
```

The addition of the flag '-c' exports access and refresh tokens using the credentials format compatible with the Google 'Storage' class.

```bash
credulous --secret path/to/your/client_secret.json path/to/scopes -o path/to/output_file.json
```

Specify an optional output JSON file with the '-o' flag. In the absence of an output file, the current client_secret file will be overwritten.

## Credentials

Go to <https://console.developers.google.com/> to create a project and get your
API credentials. You can follow step 1 of the instructions on 
[this](https://developers.google.com/gmail/api/quickstart/python)
page to get your credentials as a json.

## Scopes

You need to create a scopes file, which is a json file containing a list of
scopes that you want to authorise. For example, if you want to use the Gmail
API, you should have something like this in `scopes.json`:

```json
{
  "scopes": {
    "google": [
        "https://mail.google.com"
      ]
  }
}
```

<!-- ## Usage

You can now configure your `client` like this, for example:

```python
Also coming soon

``` -->
