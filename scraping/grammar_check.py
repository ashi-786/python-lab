import language_tool_python

# Create a tool for English (can be 'fr', 'de', etc. for French, German...)
# tool = language_tool_python.LanguageTool('en-US')
tool = language_tool_python.LanguageToolPublicAPI('en-US')

# Example text (you can load from a file or input up to 1000 words)
text = "He go to the office every day. Their is a mistake in this sentence.\nA apple a day keeps doctor away. She don't like coffee. I wany an cat but the the girl next door want a puppy."

# Check for grammar and style issues
matches = tool.check(text)

# Display issues
for match in matches:
    print(f"Issue: {match.ruleId}")
    print(f"Message: {match.message}")
    print(f"Suggestion: {match.replacements}")
    print(f"Context: {text[match.offset:match.offset + match.errorLength]}")
    print("-" * 40)

# Optional: Apply corrections
corrected_text = language_tool_python.utils.correct(text, matches)
print("\nCorrected Text:\n", corrected_text)
