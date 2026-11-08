# GitHub Actions AWS Secrets Authentication Test

This project demonstrates how a GitHub Actions workflow can retrieve application credentials from AWS Secrets Manager and use them in a Python authentication check. The workflow avoids storing the credentials directly in the repository or as GitHub Actions secrets.

## What it does

On every push to the `main` branch, the workflow:

1. Checks out this repository.
2. Uses GitHub's OIDC identity to assume an AWS IAM role.
3. Reads `AUTH_USER` and `AUTH_PASS` from a JSON secret in AWS Secrets Manager.
4. Makes those values available to the job as environment variables.
5. Runs `auth_test.py`, which sends an HTTP Basic Authentication request to httpbin.org.
6. Reports whether authentication succeeded. The script does not print the credential values.

The check succeeds when httpbin.org accepts the supplied credentials. The workflow needs access to AWS and the runner needs network access to httpbin.org.

## Requirements

- An AWS account and an AWS Secrets Manager secret containing JSON with `AUTH_USER` and `AUTH_PASS` keys.
- An IAM role that trusts GitHub Actions through OIDC and allows the workflow to call `secretsmanager:GetSecretValue` for that secret.
- A GitHub Actions workflow run on the `main` branch.
- Python 3.12 for the CI run. The script uses only the Python standard library, so no package installation is needed.

## Configure AWS and GitHub Actions

Update `.github/workflows/auth-ci.yml` before using this workflow:

- Replace `<<ACCOUNT_ID>>` in the `role-to-assume` ARN with your AWS account ID.
- Change `my-app-secrets` to the name or ARN of your Secrets Manager secret.
- Confirm `eu-west-2` matches the region where the secret is stored.
- Configure the IAM role's OIDC trust policy to allow this repository and branch, and grant it permission to read the selected secret.

The secret's `SecretString` should be JSON in this shape:

```json
{
  "AUTH_USER": "your-test-username",
  "AUTH_PASS": "your-test-password"
}
```

The workflow requires the `id-token: write` permission to request an OIDC token. Avoid putting actual credentials in the workflow file or committing them to the repository.

## Run locally

Set `AUTH_USER` and `AUTH_PASS` in your shell, then run `python auth_test.py`.

PowerShell:

```powershell
$env:AUTH_USER = "your-test-username"
$env:AUTH_PASS = "your-test-password"
python auth_test.py
```

Bash:

```bash
export AUTH_USER="your-test-username"
export AUTH_PASS="your-test-password"
python auth_test.py
```

The local script does not retrieve credentials from AWS; that retrieval is performed by the GitHub Actions workflow. Do not enter production credentials for this test: the script sends them to httpbin.org as an authentication test.

## Expected behavior

- Missing either environment variable: exits with a message identifying the missing configuration.
- Successful request: prints a success message, the HTTP status, and httpbin's authentication result.
- HTTP authentication error or request/response parsing failure: exits with a failure message.
