Changelog
=========

3.0.0 (2017-10-31)
------------------

- Store attachments as blobs.  For example the original email message.  [maurits]

- Drop support for Python 2.4, because we use ``plone.api``.
  Officially drop support for 2.6 too, and for Plone 4.2 and earlier, but it may still work.
  [maurits]

- Use plone.api to adopt a different user and roles.
  This is cleaner, and should avoid problems where the faked user did not have a user id.
  [maurits]


2.0.1 (2017-08-18)
------------------

- Log the sender and subject at info level.
  [maurits]

- Caught several cases where the created issue was invalid.
  This caused a workflow exception, which means the issue was never added.
  This could happen when an html mail was received and the mime type was not allowed in the details field.
  Now we convert the mail text to the default issue mime type.
  If the issue is still invalid, we catch the workflow exception and create the issue anyway,
  because there is no easy way of signalling this to the sender.
  The issue then has the ``new`` state, which may not be visible in the Poi user interface though.
  [maurits]


2.0 (2017-01-02)
----------------

- Check ``NEEDED_PERMISSIONS`` before faking a manager.  If a user
  already has the needed permissions, there is no need to fake a
  manager.  [maurits]

- Fake a ``TrackerManager`` instead of ``Manager`` when possible.
  This role was introduced in Products.Poi 2.2 (Plone 4).  This is
  done when ``FAKE_MANAGER`` is true, which is the default.  This only
  happens for specified IP-addresses.  [maurits]

- Fixed issue creation for Plone 4.  Posting an issue would fail
  because no ``post`` transition was available.  This is because in
  Plone 4 this happens automatically on the
  ``IObjectInitializedEvent``.  Now we only do the transition if the
  review state is still ``new``.  [maurits]


1.13 (2016-12-09)
-----------------

- Fixed package: don't use symlinks.  [maurits]


1.12 (2016-12-09)
-----------------

- Do more decoding.  Each part can have its own encoding.  We should
  use those to make something readable.  [maurits]

- Decode from quoted printable in a few cases.  [maurits]


1.11 (2012-10-14)
-----------------

- Moved to https://github.com/collective/poi.receivemail
  [maurits]


1.10 (2011-12-14)
-----------------

- Fixed wrong match for issue by subject.  While searching for #123 in
  the subject line we would match 123 at the beginning of the line as
  well, which may give wrong matches.
  [maurits]


1.9 (2011-11-28)
----------------

- Use the body charset to decode the body text and then encode it as
  utf-8 before storing it.
  [maurits]

- Avoid a unicode error when there is no body.
  [maurits]

- Optionally add attachments from the e-mail.  We look for binary
  attachments.  These are added as separate responses, as you can only
  add one attachment per issue or response.  In config.py we have
  added a setting ADD_ATTACHMENTS for this (default True) to make it a
  bit easier to switch this off in case of problems or when you do not
  want it.
  [maurits]

- Fixed handling multipart messages that have parts that themselves
  are multipart.
  [maurits]

- When there is an empty or missing Subject line, use '[no subject]'
  as title.  We do not try to match such a mail to a previous issue
  but always create a new one.
  [maurits]


1.8 (2011-11-10)
----------------

- Set more fields explicitly, as the createObjectByType call only sets
  some of them.
  [maurits]


1.7 (2011-11-09)
----------------

- When a subject (keyword, category) is given, set that explicitly.
  [maurits]

- In ``get_addresses`` allow getting addresses from headers other than
  To and From as well.
  [maurits]


1.6 (2011-09-06)
----------------

- Prevent issues from being automatically renamed after they are
  edited.
  [maurits]

- Prevent some more lower-case email address comparison problems.
  [maurits]


1.5 (2011-06-22)
----------------

- Make e-mail from address lower-case to prevent search problems with ldap
  users. [jladage]


1.4 (2011-06-14)
----------------

- When searching PAS for a user by email address, strip off any white
  space (like possibly '\r\n' in ldap) from the returned addresses, to
  avoid non-matching for silly reasons.
  [maurits]

- Moved all options to a new config.py file.
  [maurits]

- Add option ADVANCED_SUBJECT_MATCH.  Default is False: we only check
  for '#123' in the Subject line, to avoid matching overly generic
  Subject lines like 'Hi' or 'Problem'.  To get back the previous
  behavior, set this to True (in a patch in your own code, likely).
  [maurits]

- If the subject is empty, do not try to find a matching issue, as all
  issues will match.
  [maurits]


1.3 (2011-05-11)
----------------

- Added FAKE_MANAGER option (default is True) to determine if we
  should fake a Manager role to be sure that a post succeeds.
  [maurits]

- While switching users: if 'email' is not in the properties (say:
  ldap), we can get far too many results; so we do a double check.
  [maurits]


1.2 (2011-05-09)
----------------

- Ignore mails with the email_from_address as From address, as this
  too easily means that a message sent by Poi ends up being added as a
  reply on an issue that we have just created.
  [maurits]


1.1 (2011-05-05)
----------------

- Handle encoded subject lines better.
  [maurits]


1.0 (2011-05-05)
----------------

- Initial release
