def generate_prompt(template_text, user, form_data=None):
    values = {
        "business_name": None,
        "business_type": None,
        "business_location": None,
        "target_audience": None,
    }

    # 1. Pull from Profile if available
    if user.is_authenticated and hasattr(user, "profile"):
        profile = user.profile
        values.update(
            {
                "business_name": profile.business_name,
                "business_type": profile.business_type,
                "business_location": profile.business_location,
                "target_audience": profile.target_audience,
            }
        )

    # 2. Override with form input if provided
    if form_data:
        for k in values.keys():
            if form_data.get(k):
                values[k] = form_data.get(k)

    # 3. Replace placeholders; leave as [placeholder] if still empty
    for key, val in values.items():
        placeholder = f"[{key}]"
        template_text = template_text.replace(placeholder, val or placeholder)

    return template_text
