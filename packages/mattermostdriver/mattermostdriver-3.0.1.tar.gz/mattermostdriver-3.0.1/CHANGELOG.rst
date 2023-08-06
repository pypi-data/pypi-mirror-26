3.0.1
'''''
Thanks to SmartHoneyBee!
 - Changed setup of the logger #14

3.0.0
'''''
 - Removed python 3.3 from supported versions
 - Add data_retention endpoint

2.3.0
'''''
Make a `basepath` available in `Client.make_request()`.
This is mainly needed for calling `/hooks`.

2.2.0
'''''
Support for personal access tokens and MFA Token.

2.0.0
'''''

Breaking change for file uploads.
Instead of a `data` dict containing all formdata,
a `files` dict is in the following endpoints
 - emoji
  - `create_custom_emoji()` takes `emoji_name` additionally to a `files` dict
 - files
  - `upload_file()` takes `channel_id` additionally to a `files` dict
 - brand
  - `upload_brand_image()`
 - saml
  - `upload_idp_certificate()`
  - `upload_public_certificate()`
  - `upload_private_key()`
 - system
  - `upload_license_file()`
 - users
  - `set_user_profile_image()`

See the documentation for an example.