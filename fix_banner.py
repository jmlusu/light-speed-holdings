with open("C:\\Users\\jmlus\\light-speed-holdings\\src\\pages\\SolutionsPage.tsx", "r") as f:
    content = f.read()

# Find the pattern: '      />\n\n      <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-12 pb-8">'
insertion_marker = (
    '      />\n\n      <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-12 pb-8">'
)
new_banner = """      />
      {H/* H-A-O-M-T-G-V Framework Banner */}
      <div className="mt-3 mb-4 flex items-center gap-2 rounded-full border bg-ls-navy/10 text-ls-navy text-xs font-bold tracking-widest uppercase px-4 py-1.5">
        H—Human | A—Agents | O—Orchestration | M—Memory | T—Tools | G—Governance | V—Value
      </div>\n\n"""

if insertion_marker in content:
    new_content = content.replace(insertion_marker, new_banner + content.split(insertion_marker)[1])
    content = new_content
    print("Inserted banner correctly")
else:
    print("Insertion marker not found")
    # Try alternative: find '      />' and insert banner before section
    idx = content.find("      />")
    if idx >= 0:
        after_tag = content[idx + 6 :]
        sec_idx = after_tag.find(
            '\n\n      <section className="px-4 sm:px-8 max-w-7xl mx-auto w-full pt-12 pb-8">'
        )
        if sec_idx >= 0:
            before_section = after_tag[:sec_idx]
            after_section = after_tag[sec_idx:]
            new_after = before_section + new_banner + after_section
            content = content[: idx + 6] + new_after
            print("Inserted banner using alternative method")
        else:
            print("Could not find section tag after PageIntro close")
    else:
        print("Could not find '      />' in content")

# Write the modified content back
with open("C:\\Users\\jmlus\\light-speed-holdings\\src\\pages\\SolutionsPage.tsx", "w") as f:
    f.write(content)
print("File written successfully")
