import asyncio
from bs4 import BeautifulSoup
from app.shared.http_client import http_client

async def debug_unstop():
    url = "https://unstop.com/hackathons"
    
    print(f"Fetching: {url}\n")
    html = await http_client.get(url)
    
    # Save HTML to file for inspection
    with open("unstop_debug.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ Saved HTML to: unstop_debug.html")
    print(f"HTML length: {len(html)} characters\n")
    
    # Parse and find links
    soup = BeautifulSoup(html, 'lxml')
    
    all_links = soup.find_all('a', href=True)
    print(f"Total <a> tags found: {len(all_links)}\n")
    
    # Find competition/hackathon links
    event_links = []
    for link in all_links:
        href = link.get('href', '')
        if '/competitions/' in href or '/hackathons/' in href:
            event_links.append(href)
    
    print(f"Event links found: {len(event_links)}\n")
    
    if event_links:
        print("Sample event links:")
        for link in event_links[:5]:
            print(f"  - {link}")
    else:
        print("❌ NO EVENT LINKS FOUND!")
        print("\nLet's check what links we DO have:")
        for link in all_links[:10]:
            print(f"  - {link.get('href', 'NO HREF')}")

if __name__ == "__main__":
    asyncio.run(debug_unstop())
