# Certificate Setup for AudioKit Dev SF Integration

## Required Certificate: WinCAG2ANDclass2root.pem

For the AudioKit Dev SF integration to work properly, you need to obtain and place the `WinCAG2ANDclass2root.pem` certificate file in the project root directory.

### Steps to Setup Certificate:

1. **Obtain the Certificate**: Contact your system administrator or the AudioKit Dev SF team to get the `WinCAG2ANDclass2root.pem` certificate file.

2. **Place the Certificate**: Copy the certificate file to the project root directory:
   ```
   /Users/ivdulov/Documents/code-projects/ag_demo_client/WinCAG2ANDclass2root.pem
   ```

3. **Verify Certificate Format**: The certificate should be in PEM format and contain content like:
   ```
   -----BEGIN CERTIFICATE-----
   [certificate content]
   -----END CERTIFICATE-----
   ```

### Configuration Reference:

The `config_audiokit_dev_sf.ini` file has been updated to reference this certificate:
```ini
ca_cert_path = "WinCAG2ANDclass2root.pem"
```

### Testing:

After placing the certificate, test the connection with:
```bash
python -m audiogram_cli.main --config config_audiokit_dev_sf.ini models
```

### Security Note:

The certificate file is ignored by git for security reasons. Each developer needs to obtain and place their own copy of the certificate file locally.
