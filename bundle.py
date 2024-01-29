import os
from pathlib import Path
from csscompressor import compress as css_minify
from rjsmin import jsmin

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

    with open(out_file, 'w') as out_file:
        out_file.write(compressed_data)

    org_size = len(combined_data.encode('utf-8'))
    new_size = os.path.getsize(out_file.name)

    print(f'=> {out_file}')
    print(f'Original: {org_size / 1024:.2f} kB')
    print(f'Compressed: {new_size / 1024:.2f} kB')
    print(f'Reduction: {(org_size - new_size) / org_size * 100:.1f}%\n')

# Example usage:
compress(
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
compress(
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
