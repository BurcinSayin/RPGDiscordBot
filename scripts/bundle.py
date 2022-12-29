import os
import zipfile


def create_lambda_bundle():
    zf = zipfile.ZipFile("lambda.zip", "w", zipfile.ZIP_DEFLATED)
    add_folder(zf, "../commands", "commands", ".py")
    add_folder(zf, "../data", "data", ".py")
    # add_folder(zf, "../sheetdata", "sheetdata", ".py")
    add_folder(zf, "../utils", "utils", ".py")
    add_file(zf, "../lambda_function.py", None)
    add_file(zf, "../sheet-auth.json", None)
    zf.close()


def create_layer_bundle():
    zf = zipfile.ZipFile("layer.zip", "w", zipfile.ZIP_DEFLATED)
    add_folder(zf, "../lambda_layer", "python\\lib\\python3.9\\site-packages", None)
    zf.close()


def add_folder(target_zip, src_folder, zip_folder, file_filter):
    for dirname, subdir, files in os.walk(src_folder):
        relative_zip_folder = dirname.replace(src_folder, zip_folder)
        for filename in files:
            if file_filter is None:
                add_file(target_zip, os.path.join(dirname, filename), relative_zip_folder)
            else:
                if filename.endswith(file_filter):
                    add_file(target_zip, os.path.join(dirname, filename), relative_zip_folder)


def add_file(target_zip, src_file, zip_folder):
    abs_name = os.path.abspath(src_file)
    zip_name = os.path.basename(abs_name)
    if zip_folder is not None:
        zip_name = zip_folder + "\\" + os.path.basename(abs_name)
    print("zipping %s as %s", abs_name, zip_name)
    target_zip.write(abs_name, zip_name)


if __name__ == "__main__":
    create_lambda_bundle()
    create_layer_bundle()
