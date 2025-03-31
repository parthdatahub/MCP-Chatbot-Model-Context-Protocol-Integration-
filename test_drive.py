from mcp_google_drive import list_drive_files

print("🔍 Fetching your Google Drive files...")

files = list_drive_files()

print("✅ Files Found:")
for f in files:
    print(f" - {f}")
