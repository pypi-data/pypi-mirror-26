# awstwitter
Securely store Twitter API credentials in AWS EC2 Systems manager.

The secret credentials are encrypted using KMS.

Usage:

```python
import awstwitter

credentials = awstwitter.retrieve_credentials('my_namespace')

print 'consumer_key', credentials['consumer_key']
print 'consumer_secret', credentials['consumer_secret']
print 'access_token', credentials['access_token']
print 'access_token_secret', credentials['access_token_secret']
```


