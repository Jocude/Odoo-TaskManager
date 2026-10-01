def post_init_hook(env):
    """Si el español está cargado, deja al administrador en español y con la hora de Madrid."""
    if env["res.lang"]._lang_get("es_ES"):
        env.ref("base.user_admin").write({"lang": "es_ES", "tz": "Europe/Madrid"})
