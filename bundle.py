import os, time, hashlib
from pathlib import Path
from csscompressor import compress as css_minify
from rjsmin import jsmin

def generate_hash(file_path):
    unique_info = str(time.time()).encode('utf-8')
    return hashlib.md5(unique_info).hexdigest()[:8]

def remove_old_files():
    gen_folder = 'static/gen'
    if os.path.exists(gen_folder):
        for file_name in os.listdir(gen_folder):
            file_path = os.path.join(gen_folder, file_name)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print("old filed deleted")
            except Exception as e:
                print(f"Error while deleting {file_path}: {e}")

def compress(in_files, out_file, in_type='js', verbose=False):
    combined_data = ''
    
    for f in in_files:
        with open(f, 'r') as file:
            data = file.read() + '\n'
            combined_data += data
            print(f' + {f}')

    if in_type == 'js':
        compressed_data = jsmin(combined_data)
    elif in_type == 'css':
        compressed_data = css_minify(combined_data)
    else:
        raise ValueError("Invalid input type. Use 'js' or 'css'.")

    # Create the directory if it doesn't exist
    Path(out_file).parent.mkdir(parents=True, exist_ok=True)

    # Write the compressed data to the output file
    with open(out_file, 'w') as out_file_writer:
       out_file_writer.write(compressed_data)

    # Append hash to the filename for cache-busting
    hash_suffix = generate_hash(compressed_data.encode('utf-8'))
    out_file_path = Path(out_file)
    out_file_with_hash = f"{out_file_path.stem}-{hash_suffix}{out_file_path.suffix}"
    out_file_path_with_hash = out_file_path.parent / out_file_with_hash
    
    os.rename(out_file, out_file_path_with_hash)

    org_size = len(combined_data.encode('utf-8'))
    new_size = os.path.getsize(out_file_path_with_hash)

    print(f'=> {out_file_path_with_hash}')
    print(f'Original: {org_size / 1024:.2f} kB')
    print(f'Compressed: {new_size / 1024:.2f} kB')
    print(f'Reduction: {(org_size - new_size) / org_size * 100:.1f}%\n')

    return out_file_with_hash

def replace_file_references(file_path, file_id, new_file_name, type):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    found = False
    new_line = f'<link rel="stylesheet" href="/static/gen/{new_file_name}" id="{file_id}" />\n'
    if type == 'js':
        new_line = f'<script type="text/javascript" src="/static/gen/{new_file_name}" id="{file_id}"></script>\n'

    for i, line in enumerate(lines):
        if f'id="{file_id}"' in line:
            found = True
            # Replace the line with the new line
            lines[i] = new_line
            break

    if not found:
        print(f'Error: ID "{file_id}" not found in the file.')

    with open(file_path, 'w') as file:
        file.writelines(lines)

    print('write layout done')


remove_old_files()
# Example usage:
css = compress(
    [
        "static/css/font-awesome.min.css",
        "static/css/bootstrap.css",
        "static/css/owl.carousel.css",
        "static/css/responsive.css",
        "static/css/style.css",
    ],
   'static/gen/packed.css',
   in_type='css',
   verbose=True
)
js = compress(
    [
        "static/js/bootstrap.js",
        "static/js/jquery.easing.1.3.min.js",
        "static/js/jquery.sticky.js",
        "static/js/bxslider.min.js",
        "static/js/owl.carousel.min.js",
        "static/js/script.slider.js",
        "static/js/main.js",
    ],
   'static/gen/packed.js',
   in_type='js',
   verbose=True
)

layout_html_path = 'templates/layout.html'
replace_file_references(layout_html_path, 'static_gen_packed_css', css, 'css')
replace_file_references(layout_html_path, 'static_gen_packed_js', js, 'js')
