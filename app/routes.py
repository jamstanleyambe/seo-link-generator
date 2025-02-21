# import os
# import pandas as pd
# import pickle
# from flask import request, jsonify, send_file, render_template
# from app import app

# class SEOLinkGenerator:
#     def __init__(self, input_file: str = None):
#         self.input_file = input_file
#         self.output_directory = app.config['OUTPUT_FOLDER']
#         self.output_pkl_file = os.path.join(self.output_directory, "final_result.pkl")
#         self.output_csv_file = os.path.join(self.output_directory, "final_result.csv")
#         self.ensure_output_directory()

#     def ensure_output_directory(self):
#         os.makedirs(self.output_directory, exist_ok=True)

#     def clean_text(self, text: str) -> str:
#         return "" if pd.isna(text) else str(text).strip()

#     def process_keywords(self, keywords: str):
#         return [] if pd.isna(keywords) else [k.strip() for k in str(keywords).split(',') if k.strip()]

#     def create_link(self, url: str, keyword: str) -> str:
#         return f'<a href="{url}" rel="dofollow">{keyword}</a>'

#     def process_file(self) -> pd.DataFrame:
#         if not self.input_file:
#             raise ValueError("No input file specified")

#         try:
#             df = pd.read_csv(self.input_file)
#             df.columns = [col.strip().lower() for col in df.columns]

#             url_columns = ['product_url', 'products_links', 'proudcts_links', 'url', 'link', 'a']
#             keyword_columns = ['keywords', 'rank_math_focus_keyword', 'focus_keyword', 'b']

#             url_col = next((col for col in url_columns if col in df.columns), None)
#             keyword_col = next((col for col in keyword_columns if col in df.columns), None)

#             if not url_col or not keyword_col:
#                 raise ValueError(f"Missing required columns. Found: {df.columns.tolist()}")

#             expanded_data = []
#             for _, row in df.iterrows():
#                 url = self.clean_text(row[url_col])
#                 keywords = self.process_keywords(row[keyword_col])

#                 for keyword in keywords:
#                     expanded_data.append({"Keyword": keyword, "SEO Link": self.create_link(url, keyword)})

#             final_result = pd.DataFrame(expanded_data, columns=["Keyword", "SEO Link"])
#             final_result.to_pickle(self.output_pkl_file)
#             final_result.to_csv(self.output_csv_file, index=False)

#             return final_result

#         except Exception as e:
#             print(f"❌ Error processing file: {str(e)}")
#             return pd.DataFrame()

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/upload", methods=["POST"])
# def upload_file():
#     if "file" not in request.files:
#         return jsonify({"error": "No file provided"}), 400

#     file = request.files["file"]
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#     file.save(file_path)

#     generator = SEOLinkGenerator(file_path)
#     processed_file = generator.process_file()

#     if processed_file.empty:
#         return jsonify({"error": "File processing failed"}), 400

#     return jsonify({"message": "File processed successfully", "download_link": "/download"})

# @app.route("/download", methods=["GET"])
# def download_file():
#     file_path = os.path.abspath(os.path.join(app.config['OUTPUT_FOLDER'], "final_result.csv"))


#     if not os.path.exists(file_path):
#         print("❌ File not found:", file_path)
#         return jsonify({"error": "File not found"}), 404

#     print("✅ Sending file:", file_path)
#     return send_file(file_path, as_attachment=True)


import os
import pandas as pd
import pickle
from flask import request, jsonify, send_file, render_template
from app import app

class SEOLinkGenerator:
    def __init__(self, input_file: str = None):
        self.input_file = input_file
        self.output_directory = app.config['OUTPUT_FOLDER']
        self.ensure_output_directory()
        
        # Use the input file name (if provided) to generate output file names
        base_name = os.path.splitext(os.path.basename(self.input_file))[0] if self.input_file else "final"
        self.output_pkl_file = os.path.join(self.output_directory, f"{base_name}_result.pkl")
        self.output_csv_file = os.path.join(self.output_directory, f"{base_name}_result.csv")

    def ensure_output_directory(self):
        os.makedirs(self.output_directory, exist_ok=True)

    def clean_text(self, text: str) -> str:
        return "" if pd.isna(text) else str(text).strip()

    def process_keywords(self, keywords: str):
        return [] if pd.isna(keywords) else [k.strip() for k in str(keywords).split(',') if k.strip()]

    def create_link(self, url: str, keyword: str) -> str:
        return f'<a href="{url}" rel="dofollow">{keyword}</a>'

    def process_file(self) -> pd.DataFrame:
        if not self.input_file:
            raise ValueError("No input file specified")

        try:
            df = pd.read_csv(self.input_file)
            df.columns = [col.strip().lower() for col in df.columns]

            url_columns = ['product_url', 'products_links', 'proudcts_links', 'url', 'link', 'a']
            keyword_columns = ['keywords', 'rank_math_focus_keyword', 'focus_keyword', 'b']

            url_col = next((col for col in url_columns if col in df.columns), None)
            keyword_col = next((col for col in keyword_columns if col in df.columns), None)

            if not url_col or not keyword_col:
                raise ValueError(f"Missing required columns. Found: {df.columns.tolist()}")

            expanded_data = []
            for _, row in df.iterrows():
                url = self.clean_text(row[url_col])
                keywords = self.process_keywords(row[keyword_col])
                for keyword in keywords:
                    expanded_data.append({"Keyword": keyword, "SEO Link": self.create_link(url, keyword)})

            final_result = pd.DataFrame(expanded_data, columns=["Keyword", "SEO Link"])
            final_result.to_pickle(self.output_pkl_file)
            final_result.to_csv(self.output_csv_file, index=False)

            return final_result

        except Exception as e:
            print(f"❌ Error processing file: {str(e)}")
            return pd.DataFrame()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    generator = SEOLinkGenerator(file_path)
    processed_file = generator.process_file()

    if processed_file.empty:
        return jsonify({"error": "File processing failed"}), 400

    # Return the generated output file name in the download link
    output_file_name = os.path.basename(generator.output_csv_file)
    download_link = f"/download?file={output_file_name}"
    return jsonify({"message": "File processed successfully", "download_link": download_link})

@app.route("/download", methods=["GET"])
def download_file():
    # Get the output file name from the query parameters
    file_name = request.args.get('file', None)
    if not file_name:
        return jsonify({"error": "No file specified"}), 400

    file_path = os.path.abspath(os.path.join(app.config['OUTPUT_FOLDER'], file_name))
    if not os.path.exists(file_path):
        print("❌ File not found:", file_path)
        return jsonify({"error": "File not found"}), 404

    print("✅ Sending file:", file_path)
    return send_file(file_path, as_attachment=True)
