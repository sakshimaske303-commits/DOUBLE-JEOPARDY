import os

RESIZE_SCRIPT = """
<script>
window.addEventListener('load', function() {
    setTimeout(function() {
        if (typeof map !== 'undefined' && map.updateSize) {
            map.updateSize();
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

    if "map.updateSize" in content:
        print(f"Already patched: {folder_name}")
        return

    content = content.replace("</body>", RESIZE_SCRIPT + "</body>")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Patched: {folder_name}")


def main():
    for folder in MAP_FOLDERS:
        inject_resize_fix(folder)


if __name__ == "__main__":
    main()