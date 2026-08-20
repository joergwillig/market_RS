@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    group: str = "all",
    sort: str = "rel_1m",
    dir: str = "desc",
    username: str = Depends(verify_password),
):
    data = list(_cache["data"] or [])

    if group != "all":
        data = [d for d in data if d["group"] == group]

    reverse = dir != "asc"

    def key_fn(x):
        v = x.get(sort)
        if v is None:
            return -9999 if reverse else 9999
        return v

    try:
        data = sorted(data, key=key_fn, reverse=reverse)
    except Exception:
        pass

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "data": data,
            "groups": list(TICKERS.keys()),
            "active_group": group,
            "sort": sort,
            "dir": dir,
            "last_update": _cache["timestamp"].strftime("%Y-%m-%d %H:%M") if _cache["timestamp"] else "-",
        },
    )