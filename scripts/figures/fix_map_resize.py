import os

RESIZE_SCRIPT = """
<script>
window.addEventListener('load', function() {
    setTimeout(function() {
        // Folium names each map's global variable with a random hash
        // (e.g. map_bbe0fe6...), so there's no fixed "map" variable to
        // check for -- and Leaflet's resize call is invalidateSize(), not
        // updateSize() (that's OpenLayers). Scan window for whatever
        // Leaflet map instances actually exist and resize each of them.
        for (var key in window) {
            try {
                if (window[key] instanceof L.Map) {
                    window[key].invalidateSize();
                }
            } catch (e) {}
        }
    }, 300);
});
</script>
"""

MAP_FOLDERS = [
    "maldives_slr_exposure_webmap",
    "lakshadweep_slr_exposure_webmap",
    "seychelles_slr_exposure_webmap",
    "fiji_slr_exposure_webmap",
    "canary_slr_exposure_webmap",
    "maldives_ecosystem_buffer_webmap",
    "fiji_ecosystem_buffer_webmap",
    "seychelles_ecosystem_buffer_webmap",
    "lakshadweep_ecosystem_buffer_webmap",
    "canary_ecosystem_buffer_webmap",
]

STATIC_DIR = "static"


def inject_resize_fix(folder_name):
    index_path = os.path.join(STATIC_DIR, folder_name, "index.html")

    if not os.path.exists(index_path):
        print(f"NOT FOUND: {index_path}")
        return

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "invalidateSize" in content:
        print(f"Already patched: {folder_name}")
        return

    if "map.updateSize" in content:
        # strip the old, broken snippet (wrong variable name, wrong API —
        # OpenLayers' updateSize() instead of Leaflet's invalidateSize())
        # before injecting the corrected one, so both never coexist
        old_start = content.find("\n<script>\nwindow.addEventListener('load'")
        old_end = content.find("</script>\n", old_start)
        if old_start != -1 and old_end != -1:
            content = content[:old_start] + content[old_end + len("</script>\n"):]

    content = content.replace("</body>", RESIZE_SCRIPT + "</body>")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Patched: {folder_name}")


def main():
    for folder in MAP_FOLDERS:
        inject_resize_fix(folder)


if __name__ == "__main__":
    main()