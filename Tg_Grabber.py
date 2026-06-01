import os
import asyncio
from telethon import TelegramClient, errors

async def main():
    print("=" * 50)
    print("Telegram Group Media Downloader")
    print("=" * 50)
    
    # Get credentials from user
    print("\nStep 1: Enter your Telegram API credentials")
    print("(Get these from https://my.telegram.org/apps)")
    api_id = int(input("API ID: "))
    api_hash = input("API Hash: ")
    
    print("\nStep 2: Enter the group/channel link")
    print("Examples: t.me/groupname or https://t.me/+AbCdEf12345")
    group_input = input("Group link: ").strip()
    
    # Clean the link — remove https:// if present
    if group_input.startswith("https://"):
        group_input = group_input.replace("https://", "")
    
    # Create download folder
    download_dir = "downloads"
    os.makedirs(download_dir, exist_ok=True)
    
    # Start the client
    client = TelegramClient("session", api_id, api_hash)
    
    try:
        await client.start()
        user = await client.get_me()
        print(f"\nLogged in as: {user.first_name} ({user.phone})")
        
        # Get the group
        print(f"Connecting to: {group_input}...")
        entity = await client.get_entity(group_input)
        group_name = getattr(entity, "title", entity.username or "Unknown")
        print(f"Connected to: {group_name}")
        
        # Count total messages with media first
        print("\nScanning for media files...")
        total_media = 0
        async for msg in client.iter_messages(entity):
            if msg.media:
                total_media += 1
        
        print(f"Found {total_media} media files in this group")
        
        if total_media == 0:
            print("Nothing to download.")
            await client.disconnect()
            return
        
        # Ask for confirmation
        confirm = input(f"\nDownload {total_media} files? (y/n): ").lower()
        if confirm != "y":
            print("Cancelled.")
            await client.disconnect()
            return
        
        # Download
        print("\nDownloading...")
        print("-" * 50)
        downloaded = 0
        errors_count = 0
        
        async for msg in client.iter_messages(entity):
            if not msg.media:
                continue
            
            try:
                # Use original filename if available, otherwise generate one
                original_name = None
                if msg.file and msg.file.name:
                    original_name = msg.file.name
                else:
                    ext = ".bin"
                    if hasattr(msg.media, "photo"):
                        ext = ".jpg"
                    elif hasattr(msg.media, "document") and msg.media.document:
                        mime = msg.media.document.mime_type
                        ext_map = {
                            "image/jpeg": ".jpg",
                            "image/png": ".png",
                            "image/gif": ".gif",
                            "image/webp": ".webp",
                            "video/mp4": ".mp4",
                            "video/x-matroska": ".mkv",
                            "audio/mpeg": ".mp3",
                            "audio/ogg": ".ogg",
                            "audio/wav": ".wav",
                            "application/pdf": ".pdf",
                            "application/zip": ".zip",
                            "application/x-rar-compressed": ".rar",
                            "text/plain": ".txt",
                        }
                        ext = ext_map.get(mime, ".bin")
                    original_name = f"media_{msg.id}{ext}"
                
                filepath = os.path.join(download_dir, original_name)
                
                # Skip if already downloaded
                if os.path.exists(filepath):
                    print(f"[SKIP] {original_name} (already exists)")
                    continue
                
                # Download
                result = await msg.download_media(file=filepath)
                if result:
                    downloaded += 1
                    print(f"[OK]   {downloaded}/{total_media} - {original_name}")
                else:
                    errors_count += 1
                    print(f"[FAIL] Could not download message {msg.id}")
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(0.5)
                
            except errors.FloodWaitError as e:
                print(f"\n[!] Rate limited. Waiting {e.seconds} seconds...")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                errors_count += 1
                print(f"[ERROR] {e}")
        
        # Summary
        print("-" * 50)
        print(f"\nDownload complete!")
        print(f"Successfully downloaded: {downloaded}")
        print(f"Errors: {errors_count}")
        print(f"Files saved to: {download_dir}/")
        
    except errors.rpcerrorlist.UserNotParticipantError:
        print(f"\n[ERROR] You are not a member of this group.")
        print("You must join the group first before downloading.")
    except ValueError:
        print(f"\n[ERROR] Could not find the group.")
        print("Check the link and make sure you're a member.")
    except Exception as e:
        print(f"\n[ERROR] {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())