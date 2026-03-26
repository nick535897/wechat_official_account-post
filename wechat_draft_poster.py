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
        resp = urllib.request.urlopen(thumb_url, timeout=30)
        file_data = resp.read()
        content_type = resp.headers.get("Content-Type", "image/png")
        ext = content_type.split("/")[1]
        filename = f"thumb.{ext}"
        boundary = "----WebKitFormBoundary" + "x" * 16

        body = f"--{boundary}\r\n"
        body += f'Content-Disposition: form-data; name="media"; filename="{filename}"\r\n'
        body += f"Content-Type: {content_type}\r\n\r\n"
        body = body.encode() + file_data + b"\r\n--" + boundary.encode() + b"--\r\n"

        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=thumb"
        req = urllib.request.Request(url, data=body, method="POST")
        req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")

        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))

        print(f"Upload thumb response: {json.dumps(result, indent=2, ensure_ascii=False)}")
        if "media_id" in result:
            thumb_media_id = result["media_id"]
            print(f"Got thumb_media_id: {thumb_media_id}")
        else:
            print(f"Upload thumb failed")

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
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--content", required=True)
    parser.add_argument("--app-id", required=True)
    parser.add_argument("--app-secret", required=True)
    parser.add_argument("--author", default="")
    parser.add_argument("--digest", default="")
    parser.add_argument("--thumb-url")
    parser.add_argument("--access-token")
    args = parser.parse_args()

    main(
        title=args.title,
        content=args.content,
        app_id=args.app_id,
        app_secret=args.app_secret,
        author=args.author,
        digest=args.digest,
        thumb_url=args.thumb_url,
        access_token=args.access_token,
    )
