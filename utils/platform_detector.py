def detect_platform(url):
    url_lower = url.lower()
    
    platform_map = {
        ('youtube.com', 'youtu.be'): "YouTube",
        ('instagram.com',): "Instagram",
        ('tiktok.com',): "TikTok",
        ('facebook.com', 'fb.watch'): "Facebook",
        ('twitter.com', 'x.com'): "Twitter/X",
        ('vimeo.com',): "Vimeo",
        ('dailymotion.com',): "Dailymotion",
        ('reddit.com',): "Reddit",
        ('twitch.tv',): "Twitch",
        ('soundcloud.com',): "SoundCloud",
    }
    
    for domains, platform_name in platform_map.items():
        if any(domain in url_lower for domain in domains):
            return platform_name
    
    return "Other Platform"