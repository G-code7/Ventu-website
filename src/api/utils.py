from flask import jsonify, url_for

class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        return {
            'message': self.message,
            **(self.payload or {})
        }

def has_no_empty_params(rule):
    defaults = rule.defaults or ()
    arguments = rule.arguments or ()
    return len(defaults) >= len(arguments)

def generate_sitemap(app):
    links = ['/admin/']
    
    # Obtener todas las rutas válidas
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            if "/admin/" not in url:
                links.append(url)

    # Generar HTML
    links_html = "".join(f"<li><a href='{url}'>{url}</a></li>" for url in links)
    
    return f"""
    <div style="text-align: center; padding: 2rem;">
        <img src="https://e7.pngegg.com/pngimages/367/569/png-clipart-tesseract-odyssey-scala-altered-state-polaris-geometric-cover-glass-angle.png" style="max-height: 80px; margin: 1rem 0;">
        <h2>Ventu admin</h2>
        <div style="margin: 2rem 0;">
            <p>API Host: 
            <script>
                document.write('<input style="padding: 5px; width: 300px" type="text" value="'+window.location.href+'" />');
            </script>
            </p>
        </div>
        <div style="max-width: 600px; margin: 0 auto; text-align: left;">
            <ul>{links_html}</ul>
        </div>
    </div>
    """