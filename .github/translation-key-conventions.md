When generating gettext or Flask-Babel translation strings, always use symbolic translation keys instead of human-readable English sentences.

Rules:

1. Use SCREAMING_SNAKE_CASE for all translation keys.
2. Separate words with underscores.
3. Use descriptive names that clearly indicate the purpose of the message.
4. Use common suffixes such as:

   * _MSG for general messages
   * _ERROR for error messages
   * _SUCCESS_MSG for success notifications
   * _WARNING for warnings
   * _LABEL for form labels
   * _PLACEHOLDER for input placeholders
   * _TITLE for page titles
   * _DESCRIPTION for descriptions
5. Never use English sentences inside gettext calls.
6. Convert any user-facing text into a meaningful symbolic key.

Examples:

Bad:
_("User updated successfully")
_("Delete user")
_("Email address is required")

Good:
_("UPDATE_USER_SUCCESS_MSG")
_("DELETE_USER_LABEL")
_("EMAIL_ADDRESS_REQUIRED_ERROR")

Bad:
flash(_("Department created successfully"))

Good:
flash(_("CREATE_DEPARTMENT_SUCCESS_MSG"))

When modifying existing code, automatically replace human-readable gettext strings with descriptive SCREAMING_SNAKE_CASE translation keys while preserving the original meaning.

