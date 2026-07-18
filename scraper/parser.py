def parse_post(detail):
    data = {
        "features": {},
        "details": {}
    }
    seo = detail.get("seo", {})
    web_info = seo.get("web_info", {})
    location = detail.get("location", {})
    point = (
        location
        .get("exact_data", {})
        .get("point", {})
    )
    webengage = detail.get("webengage", {})
    share = detail.get("share", {})
    
    data["expires_at"] = seo.get("unavailable_after")
    data["url"] = share.get("web_url")
    data["price_number"] = webengage.get("price")
    data["business_type"] = webengage.get("business_type")
    data["latitude"] = point.get("latitude")
    data["longitude"] = point.get("longitude")
    data["city"] = web_info.get("city_persian")
    data["district"] = web_info.get("district_persian")
    data["category"] = web_info.get("category_slug_persian")

    sections = detail.get("sections", [])

    for section in sections:

        section_name = section.get("section_name")

        # ------------------ TITLE ------------------
        if section_name == "TITLE":

            for widget in section.get("widgets", []):

                if widget.get("widget_type") == "LEGEND_TITLE_ROW":
                    data["title"] = widget.get("data", {}).get("title")
        # ---------------- DESCRIPTION ----------------
        elif section_name == "DESCRIPTION":

            for widget in section.get("widgets", []):

                if widget.get("widget_type") == "DESCRIPTION_ROW":
                    data["description"] = widget.get("data", {}).get("text")
        # ---------------- LIST_DATA ----------------
        elif section_name == "LIST_DATA":

            for widget in section.get("widgets", []):

                widget_type = widget.get("widget_type")

                # متراژ، ساخت، اتاق
                if widget_type == "GROUP_INFO_ROW":

                    for item in widget.get("data", {}).get("items", []):

                        title = item.get("title")
                        value = item.get("value")

                        if title == "متراژ":
                            data["area"] = value

                        elif title == "ساخت":
                            data["year"] = value

                        elif title == "اتاق":
                            data["rooms"] = value

                # قیمت، طبقه و...
                elif widget_type == "UNEXPANDABLE_ROW":
                    
                    title = widget.get("data", {}).get("title")
                    value = widget.get("data", {}).get("value")

                    if title == "قیمت کل":
                        data["price"] = value

                    elif title == "قیمت هر متر":
                        data["price_per_meter"] = value

                    elif title == "طبقه":
                        data["floor"] = value
                elif widget_type == "GROUP_FEATURE_ROW":

                    for item in widget.get("data", {}).get("items", []):
                        title = item.get("title")
                        available = item.get("available")

                        if title is not None:
                            data["features"][title] = available
                elif widget_type == "SELECTOR_ROW":

                    title = widget.get("data", {}).get("title")

                    if title != "سایر ویژگی‌ها و امکانات":
                        continue

                    action = widget.get("data", {}).get("action", {})
                    payload = action.get("payload", {})
                    modal_page = payload.get("modal_page", {})
                    widgets = modal_page.get("widget_list", [])
                    for w in widgets:

                        if w.get("widget_type") == "UNEXPANDABLE_ROW":

                            t = w.get("data", {}).get("title")
                            v = w.get("data", {}).get("value")

                            if t:
                                data["details"][t] = v

                        elif w.get("widget_type") == "FEATURE_ROW":

                            title = w.get("data", {}).get("title")

                            if title not in data.get("features", {}):
                                data["features"][title] = True

    return data