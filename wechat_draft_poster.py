def main(title: str, content: str, app_id: str, app_secret: str, author: str = "", digest: str = "", thumb_url: str = None, access_token: str = None):
    import json
    import urllib.request

    if not access_token:
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))

        if "access_token" not in result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return

        access_token = result["access_token"]

    print(f"access_token: {access_token[:20]}...")

    thumb_media_id = None
    if thumb_url:
        url = f"https://api.weixin.qq.com/cgi-bin/media/uploadurl?access_token={access_token}&type=thumb"
        payload = json.dumps({"url": thumb_url}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, method="POST")
        req.add_header("Content-Type", "application/json")

        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))

        if "media_id" in result:
            thumb_media_id = result["media_id"]
            print(f"Got thumb_media_id: {thumb_media_id}")
        else:
            print(f"Upload thumb failed: {json.dumps(result, indent=2, ensure_ascii=False)}")

    article = {
        "title": title,
        "author": author,
        "digest": digest,
        "content": content,
        "content_source_url": "",
        "thumb_media_id": thumb_media_id,
        "need_open_comment": 0,
        "only_fans_can_comment": 0,
    }

    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}"
    payload = json.dumps({"articles": [article]}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")

    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main(
        title="测试标题",
        content="<p>正文</p>",
        app_id="wx118ca05fd5786da4",
        app_secret="f938c2e1a93c504af3ef234be848cdb9",
    )
