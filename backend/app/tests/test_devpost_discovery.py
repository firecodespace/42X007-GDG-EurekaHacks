from app.discovery.devpost_discoverer import DevpostDiscoverer


def test_devpost_discovery():
    discoverer = DevpostDiscoverer()
    urls = discoverer.discover()

    assert len(urls) > 0
    assert all(u.url.startswith("http") for u in urls)
