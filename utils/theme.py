import toml

def get_theme():
    try:
        theme = toml.load(".streamlit/config.toml").get("theme", {})
        return {
            "primary": theme.get("primaryColor", "#5ab2e6"),
            "secondary_bg": theme.get("secondaryBackgroundColor", "#63d463"),
            "background": theme.get("backgroundColor", "#f5f5f5"),
            "text": theme.get("textColor", "#0a0a0a"),
        }
    except Exception:
        return {
            "primary": "#5ab2e6",
            "secondary_bg": "#63d463",
            "background": "#f5f5f5",
            "text": "#0a0a0a",
        }