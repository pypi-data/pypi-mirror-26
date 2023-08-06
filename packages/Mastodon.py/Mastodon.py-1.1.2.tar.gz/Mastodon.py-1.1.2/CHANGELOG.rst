A note on versioning: This librarys major version will grow with the APIs 
version number. Breaking changes will be avoided as far as at all possible.

v1.1.2
------
* 2.0 id compatibility (thanks codl)
* Added emoji support
* Media alt-text support (thanks foozmeat)
* Python2 fixes (thanks ragingscholar)
* General code cleanup and small fixes (thanks codl)
* Beginnings of better error handling (thanks Elizafox)
* Various documentation updates

v1.1.1
------
 * Emergency fix to allow logging in to work (thanks codl)

v1.1.0
------
 * BREAKING CHANGE: Added date parsing to the response parser
 * Added notification dismissal
 * Added conversation muting
 * Updated documentation
 * Added asynchronous mode for the streaming API
 * Fixed several bugs (thanks ng-0, LogalDeveloper, Chronister, Elizafox, codl, lambadalambda)
 * Improved code style (thanks foxmask)

v1.0.8
------
 * Added support for domain blocks
 * Updated the documentation to reflect API changes
 * Added support for pagination (Thanks gled-rs, azillion)
 * Fixed various bugs (Thanks brrzap, fumi-san)

v1.0.7
------
 * Added support for OAuth2 (Thanks to azillon)
 * Added support for several new endpoints (Thanks phryk, aeonofdiscord, naoyat)
 * Fixed various bugs (Thanks EliotBerriot, csu, edsu)
 * Added support for streaming API (Thanks wjt)

v1.0.6
------
 * Fixed several bugs (Thanks to Psycojoker, wjt and wxcafe)
 * Added support for spoiler text (Thanks to Erin Congden)
 * Added support for mute functionality (Thanks to Erin Congden)
 * Added support for getting favourites (Thanks to Erin Congden)
 * Added support for follow requests (Thanks to Erin Congden, again)
 * Added MANIFEST.in to allow for conda packaging (Thanks, pmlandwehr)

v1.0.5
------
 * Fixed previous fix (Thank you, @tylerb@mastodon.social)

v1.0.4
------
 * Fixed an app creation bug (Thank you, @tylerb@mastodon.social)

v1.0.3
------
  * Added support for toot privacy (thanks fpietsche)

v1.0.2
------
  * Removed functions and documentation for APIs that have been removed
  * Documentation is now vastly improved thanks to @lydia@mastodon.social / girlsim
  * Rate limiting code - Mastodon.py can now attempt to respect rate limits
  * Several small bug fixes, consistency fixes, quality-of-life improvements

v.1.0.1
-------
  * Added timeline_*() functions for consistency. timeline() functions as before.
  * Clarified documentation in various places.
  * Added previously-undocumented notifications() - API that gets a users notifications.
  
v.1.0.0
-------
 * Initial Release

